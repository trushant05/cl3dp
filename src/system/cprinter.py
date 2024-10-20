# Base imports
import os
import sys
import yaml
import argparse
import time
import numpy as np
import math
import cv2

# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Get all configurations
stage_config_path = os.path.join(root_path, '..\config\stages.yaml')
controller_config_path = os.path.join(root_path, '..\config\controller.yaml')
pressure_config_path = os.path.join(root_path, '..\config\pressure.yaml')
system_config_path = os.path.join(root_path, '..\config\printer.yaml')
camera_config_path = os.path.join(root_path, '..\config\camera.yaml')

# Load all configurations
with open(stage_config_path, 'r') as file:
    stage_cfg = yaml.safe_load(file)

with open(controller_config_path, 'r') as file:
    ctrl_cfg = yaml.safe_load(file)

with open(pressure_config_path, 'r') as file:
    pressure_cfg = yaml.safe_load(file)

with open(system_config_path, 'r') as file:
    system_cfg = yaml.safe_load(file)

with open(camera_config_path, 'r') as file:
    camera_cfg = yaml.safe_load(file)

# Join root pathr
sys.path.insert(0, root_path)

# Import Aerotech and staging
from stages.stage_control import Staging, Aerotech
from vision.camera_controller import CameraController
from vision.image_grabber import ImageGrabber

class CPrinter:
    """
    A revised printer class which provides access to stages, contoller and vision.

    Attributes:
        current_location['x']           (int)    :    x-axis current observed location
        current_location['y']           (int)    :    y-axis current observed location
        current_location['z']           (int)    :    z-axis current observed location
        nozzle_position['x']            (int)    :    x-axis running nozzle location during print
        nozzle_position['y']            (int)    :    y-axis running nozzle location during print
        nozzle_position['z']            (int)    :    z-axis running nozzle location during print
        nozzle_now                      (bool)   :    Flag for operating mode (camera or nozzle)
        camera_params                   (dict)   :    Camera optical parameters
        camera_offset                   (list)   :    Camera offset after each iteration of printing
        current_pressure                (float)  :    Current set pressure of the system
        current_voltage                 (float)  :    Current voltage of the pressure system
        safe_height                     (float)  :    Set safe height for non-print x-y movement 
        speed_print                     (float)  :    Reference print speed
        speed_fast                      (float)  :    Set fast movement speed for transitions
        speed_slow                      (float)  :    Set slow movement speed for lowering to print height
        speed_camera                    (float)  :    Set camera movement speed

    """
    def __init__(self):
        """
        Initializes a new instance of Printer class.
        """
        # Initialize stages using Aerotech class
        self.staging = Aerotech(stage_cfg['substrate']['GLASS'], incremental = False)
        self.staging.send_message('~INITQUEUE\n') # Initialize the queue

        # Understood current location
        self.current_location = {
            "x":0,
            "y":0,
            "z":0
        }

        # Known Nozzle location
        self.nozzle_position = {
            "x":0,
            "y":0,
            "z":0
        }

        # Are we at the nozzle or the camera
        self.nozzle_now = True

        # Where is the camera relative to the nozzle
        self.camera_offset = system_cfg['camera_offset']

        # Camera operating parameters
        self.camera_params = camera_cfg['params']

        # Current Pressure
        self.current_pressure = 0

        # Current Voltage
        self.current_voltage = 0

        # Various Print Speed Values
        self.safe_height = 18.0
        self.speed_print = .35
        self.speed_fast = 50.0
        self.speed_slow = 0.5
        self.speed_camera = 5.0

        # Tuning Params
        self.sleep_time = 1
        self.norm_step_size = 0.5

        # Datapath
        self.data_path = 'data_temp'

        self.default_pressure = 18

        self.set_smooth_operation()

        self.levelpoints = system_cfg['four_point']


    def set_pressure(self, pressure):
        """
        Set pressure of the system by taking input PSI
        and converting that to voltage using provided
        pressure model in pressure.yaml

        Parameters:
            pressure (float)    :    Pressure to set (PSI)
        """
        voltage = pressure_cfg['params']['gain'] * pressure + pressure_cfg['params']['bias']

        if voltage < 0.1:
            self.current_voltage = voltage = 0
            self.staging.set_pressure(voltage)
            self.current_pressure = 0
        elif voltage > 5:
            voltage = 5
            self.staging.set_pressure(voltage)
            self.current_pressure = (voltage - pressure_cfg['params']['bias']) / pressure_cfg['params']['gain']
        else:
            self.staging.set_pressure(voltage)
            self.current_pressure = pressure

    def move_abs(self, x = None, y = None, z = None, f = .2, bypass = False):   
        """
        Move using absolute positioning based on home reference of system

        Parameters:
            x (float)       :    Location to move to in the x
            y (float)       :    Location to move to in the y
            z (float)       :    Location to move to in the z
            f (float)       :    Speed with which to move
            bypass (bool)   :    Bypass the nozzle reference update
        """
        # Ensure which values are populated update current location
        if x is not None:
            self.current_location["x"] = x
        if y is not None:
            self.current_location["y"] = y
        if z is not None: 
            self.current_location["z"] = z

        # Handle switch between nozzle and camera
        if not bypass:
            if self.nozzle_now: 
                # Update nozzle position
                self.nozzle_position = self.current_location
            else:
                # If we are at camera, adjust location by offset
                if x is not None:
                    x = x + self.camera_offset[0]
                if y is not None:
                    y = y + self.camera_offset[1]
                if z is not None: 
                    z = z + self.camera_offset[2]
        # Run movement
        self.staging.goto(x = x, y = y, z = z, f = f)

    def move_to_camera(self):
        """
        Method to move to camera based on the camera offset.

        """
        if self.nozzle_now:
            # Ensure pressure is off
            self.set_pressure(0)

            # Copy Nozzle Location
            self.nozzle_position = self.current_location.copy() 

            # Move in absolute so safe movement height 
            self.move_abs(z = self.safe_height, f = self.speed_fast, bypass = True)

            # Move to camera space
            self.move_abs(x = self.camera_offset[0]+self.nozzle_position["x"], y = self.camera_offset[1]+self.nozzle_position["y"], f = self.speed_fast, bypass = True)
            self.move_abs(z = self.camera_offset[1]+4, f = self.speed_fast, bypass = True)
            self.move_abs(z = self.camera_offset[2]+self.nozzle_position["z"], f = self.speed_camera, bypass = True)

            # Set to current camera
            self.nozzle_now = False

            # Wait a bit
            time.sleep(2)


    def move_to_nozzle(self):
        """
        Method to move to camera based on the camera offset.

        """
        if not self.nozzle_now:
            # Ensure pressure is off
            self.set_pressure(0) 

            # Move in absolute so safe movement height 
            self.move_abs(z = self.safe_height, f = self.speed_fast, bypass = True)
            print(f"x={self.nozzle_position['x']},  y={self.nozzle_position['y']}")
            # Move to nozzle space
            self.move_abs(x = self.nozzle_position["x"], y = self.nozzle_position["y"], f = self.speed_fast, bypass = True)
            self.move_abs(z = 4, f = self.speed_fast, bypass = True)
            self.move_abs(z = self.nozzle_position["z"], f = self.speed_camera, bypass = True)

            # Wait a bit
            time.sleep(2)

            # Set to current nozzle
            self.nozzle_now = True
            nozzle_now = self.current_location


    def grab_image_pylon(self):
        """
        Method to grab the image at the measurement camera.

        """
        # Creates a measurement camera
        camera_controller = CameraController("measurement_camera")
        camera_controller.configure_for_software_trigger()

        # Creates the image grabber 
        image_grabber = ImageGrabber(camera_controller)

        # Grab image
        image = image_grabber.grab_image()

        # Close/release it after usage
        camera_controller.stop_grabbing()
        camera_controller.close()

        return image

    def dist_ang_calc(self, p1, p2):
        # Calculate change in x and y
        dx = p2[0]-p1[0]
        dy = p2[1]-p1[1]
        
        # Calculate magnitude of direction vector
        dist = math.sqrt(dx**2 + dy**2)

        # Normalize direction vector
        if dist == 0:
            raise ValueError("Points point1 and point2 are the same")

        angle = math.atan2(dy,dx)

        return [dist, angle, [dx,dy]]

    def get_cam_points(self, points):
        # Camera width in pixels times the scale to microns
        # then microns to millimeters
        spacing = self.camera_params["width"]*1.54/1000

        res = self.get_print_points(points, step_size_mm=spacing)

        return res

    def point_on_vector(self, p1, p2, d):
        # calc dist
        dist, angle, change = self.dist_ang_calc(p1, p2)
        
        # Calculate new point coordinates
        new_x = p1[0] + (d / dist) * change[0]
        new_y = p1[1] + (d / dist) * change[1]
    
        return [new_x, new_y]

    def get_print_points(self, points, step_size_mm=0.5):
        """
        Creates a discretized set of linear vector along given points.

        """
        instructs = []
        prior = 0

        for idx in range(1, len(points)):
            # Get distance stuff
            dist, angle, change = self.dist_ang_calc(points[prior], points[idx])

            # Create spacing by step size
            spacing = math.floor(dist/step_size_mm)

            # Create equal distance magnitude
            magnitude = spacing * step_size_mm

            # Create last point of segment
            stop_point = self.point_on_vector(points[prior], points[idx], magnitude)

            # Create segment
            x, y = self.create_vector(points[prior], stop_point, spacing)

            # Append List
            XY = list(zip(x, y))
            instructs.extend(XY)

            # Update Prior
            prior += 1

        # Add final point
        final = (points[-1][0], points[-1][1])
        instructs.append(final)

        return instructs

    def create_vector(self, p1, p2, print_steps, end=False):
        """
        Creates a discretized vector along 2 points.

        """

        # Create x and y points
        listx = np.linspace(p1[0], p2[0], print_steps, endpoint=end)
        listy = np.linspace(p1[1], p2[1], print_steps, endpoint=end)

        # Round to sane values
        listx = np.around(listx, decimals=4)
        listy = np.around(listy, decimals=4)

        return [listx, listy]
    
    def save_pict(self, image, label, job):
        print("Saving Picture")
        dir_name = self.data_path
        data_path = os.path.join(root_path, dir_name)
        data_path = os.path.join(data_path, job)
        data_path = os.path.join(data_path, label)
        os.makedirs(data_path, exist_ok=True)

        t_str = time.strftime("%Y%m%d-%H%M%S")
        img_str = label + "_" + t_str + ".png"
        img_path = os.path.join(data_path, img_str)
        cv2.imwrite(img_path, image)

    def print_and_capture(self, coords, pressures, speeds, job, camera_use = True, discrete = True):

        if discrete:
            print_points = self.get_print_points(coords, step_size_mm=self.norm_step_size)
            pres_list, speed_list = self.speeds_and_pressures_block(pressures, speeds, len(print_points))
            self.set_pressure(pres_list[0])
            self.speed_print = speed_list[0]

        else:
            print_points = coords
            self.set_pressure(pressures)
            self.speed_print = speeds

        self.move_to_nozzle()
        time.sleep(self.sleep_time)


        idx = 0
        for p in print_points:
            if discrete:
                self.set_pressure(pres_list[idx])
                self.speed_print = speed_list[idx]
            else:
                self.set_pressure(pressures)
                self.speed_print = speeds
            z = self.bilinear_interpolation(p[0],p[1])
            self.move_abs(x=p[0],y=p[1], z=z, f=self.speed_print)
            idx = idx + 1
            
        self.set_pressure(0)

        self.move_to_camera()

        if camera_use:
            self.camera_run(coords, job)


    def camera_run(self, coords, job):
        camera_points = self.get_cam_points(coords)
        for p in camera_points:
            self.move_abs(x=p[0],y=p[1], f=self.speed_fast)
            img = self.grab_image_pylon()
            self.save_pict(img, "Original", job)
            _, binary = cv2.threshold(img,  0.9 * 255, 255, cv2.THRESH_BINARY)
            self.save_pict(binary, "Binary", job)

    def print_dots(self, sleeps, spacing, job="dots", camera_use = True):
        self.move_to_nozzle()
        self.move_abs(z=self.safe_height, f=self.speed_fast)
        for sleep in sleeps:
            self.nozzle_position["x"] = self.nozzle_position["x"] + spacing[0][0]
            self.nozzle_position["y"] = self.nozzle_position["y"] + spacing[0][1]
            #self.move_to_nozzle()
            self.move_abs(x=self.nozzle_position["x"], y=self.nozzle_position["y"], f=self.speed_fast)
            self.move_abs(z=2, f=self.speed_fast)
            self.move_abs(z=0, f=self.speed_slow)
            self.nozzle_now = True
            #time.sleep(3)
            self.set_pressure(18)
            time.sleep(sleep)
            self.set_pressure(0)
            #self.move_abs(z=self.safe_height, f=self.speed_fast, bypass=True)
            self.move_to_camera()

            if camera_use:
                img = self.grab_image_pylon()
                self.save_pict(img, "Original", job)
                _, binary = cv2.threshold(img,  0.9 * 255, 255, cv2.THRESH_BINARY)
                self.save_pict(binary, "Binary", job)


    def load_next_job(self, start_coords):
        self.move_to_camera()

        if start_coords[0] is not None:
            self.nozzle_position["x"] = start_coords[0]
        if start_coords[1] is not None:
            self.nozzle_position["y"] = start_coords[1]
            
        self.move_to_nozzle()

    def set_zero(self):
        self.staging.send_message('G92 X0 Y0 Z0\n')

    def update_relative_points(self, points, start):
        updated_points = []
        for point in points:
            updated_point = [point[0] + start[0], point[1] + start[1]]
            updated_points.append(updated_point)
        return updated_points
    
    def set_smooth_operation(self):
        self.staging.send_message("WAIT MODE AUTO\n")
        self.staging.send_message("VELOCITY ON\n")

    def speeds_and_pressures_block(self, pressures, speeds, map_length):
        p_split = math.floor(map_length/len(pressures))
        s_split = math.floor(map_length/len(speeds))


        res_pressures = []
        for i in range(len(pressures)):
            temp = [pressures[i]] * p_split
            res_pressures.extend(temp)

        pad = map_length - len(res_pressures)
        if pad > 0:
            temp = [pressures[-1]]*pad
            res_pressures.extend(temp)

        res_speeds = []
        for i in range(len(speeds)):
            temp = [speeds[i]] * s_split
            res_speeds.extend(temp)

        pad = map_length - len(res_speeds)
        if pad > 0:
            temp = [speeds[-1]]*pad
            res_speeds.extend(temp)

        return (res_pressures, res_speeds)


    def bilinear_interpolation(self, x, y):
        x1, y1, z1 = self.levelpoints["point0"]
        x2, y2, z2 = self.levelpoints["point1"]
        x3, y3, z3 = self.levelpoints["point2"]
        x4, y4, z4 = self.levelpoints["point3"]
        
        # Check if the points form a valid rectangle in the x-y plane
        if x1 == x2 or x3 == x4 or y1 == y4 or y2 == y3:
            raise ValueError("Points do not form a valid rectangle in the x-y plane.")
        
        # Bilinear interpolation
        if x2 != x1:
            f = (x - x1) / (x2 - x1)
        else:
            f = 0.5  # Arbitrary value when x2 == x1
        
        if y3 != y1:
            g = (y - y1) / (y3 - y1)
        else:
            g = 0.5  # Arbitrary value when y2 == y1
        
        # Calculate z based on the interpolation factors
        z = (1 - f) * (1 - g) * z1 + f * (1 - g) * z2 + f * g * z3 + (1 - f) * g * z4
        
        return z
                
    




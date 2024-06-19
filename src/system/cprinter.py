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
        xaxis                 (int)    :    x-axis identifier
        yaxis                 (int)    :    y-axis identifier
        zaxis                 (int)    :    z-axis identifier
        xspeed                (float)  :    Stage speed in x-axis
        yspeed                (float)  :    Stage speed in y-axis
        zspeed                (float)  :    Stage speed in z-axis
        zspeed_slow           (float)  :    Stage speed in z-axis (slower)
        current_x             (float)  :    Current location in x-axis
        current_y             (float)  :    Current location in y-axis
        pressure              (int)    :    Pressure of the system
        recipe                (list)   :    Recipe to print
        starting_locations    (list)   :    Base location where the printing starts
        controller            (class)  :    Instance of the controller class
        base_speed            (float)  :    Base speed when the system starts
        current_pressure      (int)    :    Current pressure of the system
        current_location      (list)   :    Current location of stages in (x, y, z)
        base_camera_offset    (list)   :    Camera offset at the start of the experiment
        camera_offset         (list)   :    Camera offset after each iteration of printing
        print_location        (list)   :    Location to print at
        moving_height         (float)  :    Height in z-axis while moving from camera <-> nozzle
        ref_width             (int)    :    Reference line width for controller
        estimated_line_width  (float)  :    Estimated line width from vision system
        staging               (int)    :    Instance of the Aerotech staging class

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

        # Current Pressure
        self.current_pressure = 0

        # Current Voltage
        self.current_voltage = 0

        # Various Print Values
        self.safe_height = 18
        self.speed_print = .27
        self.speed_fast = 50
        self.speed_slow = 0.5
        self.speed_camera = 5

        # Camera Stuff
        self.camera_params = camera_cfg['params']

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

        if x is not None:
            self.current_location["x"] = x
        if y is not None:
            self.current_location["y"] = y
        if z is not None: 
            self.current_location["z"] = z

        if not bypass:
            if self.nozzle_now: 
                self.nozzle_position = self.current_location
            else:
                if x is not None:
                    x = x + self.camera_offset[0]
                if y is not None:
                    y = y + self.camera_offset[1]
                if z is not None: 
                    z = z + self.camera_offset[2]

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
        camera_controller = CameraController("measurement_camera")
        camera_controller.configure_for_software_trigger()

        image_grabber = ImageGrabber(camera_controller)
        image = image_grabber.grab_image()

        camera_controller.stop_grabbing()
        camera_controller.close()

        return image

    def dist_ang_calc(self, p1, p2):

        dist = self.camera_params["px_mm"]*math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
        angle = math.atan2((p2[1]-p1[1]),(p2[0]-p1[0]))

        return [dist, angle]

    def get_cam_points(self, points):
        spacing = self.camera_params["width"]*1.54/1000
        res = 1
        prior = 0
        for idx in range(1, len(points)):
            dist, angle = self.dist_ang_calc(points[prior], points[idx])

        if dist > spacing:
            res = math.floor(dist/spacing)
            prior += 1

        return res

    def get_print_points(self, points):
        spacing = 100*1.54/1000
        res = 1
        prior = 0
        for idx in range(1, len(points)):
            dist, angle = self.dist_ang_calc(points[prior], points[idx])

        if dist > spacing:
            res = math.floor(dist/spacing)
            prior += 1

        return res

    def create_vector(self, p1, p2, camera=False):
        point_div = 1
        if camera:
            point_div = self.get_cam_points([p1,p2])
        else:
            point_div = self.get_print_points([p1,p2])

        listx = np.linspace(p1[0], p2[0], point_div, endpoint=False)
        listy = np.linspace(p1[1], p2[1], point_div, endpoint=False)

        listx = np.around(listx, decimals=4)
        listy = np.around(listy, decimals=4)

        return [listx, listy]
    
    def save_pict(self, image, label, job):
        print("Saving Picture")
        dir_name = 'data_temp'
        data_path = os.path.join(root_path, dir_name)
        data_path = os.path.join(data_path, job)
        data_path = os.path.join(data_path, label)
        os.makedirs(data_path, exist_ok=True)

        t_str = time.strftime("%Y%m%d-%H%M%S")
        img_str = label + "_" + t_str + ".png"
        img_path = os.path.join(data_path, img_str)
        cv2.imwrite(img_path, image)

    def print_and_capture(self, coords, pressure, job, camera_use = True):
        self.move_to_nozzle()
        self.set_pressure(pressure)
        time.sleep(1)
        for i in range(1, len(coords)):
            xv,yv = self.create_vector(coords[i-1], coords[i])
            #self.set_pressure(pressures[0])
            for idx in range(len(xv)):
                #print(f"x={xv[idx]},y={yv[idx]}, f={speed_slow}")
                self.move_abs(x=xv[idx],y=yv[idx], f=self.speed_slow)
        self.set_pressure(0)

        self.move_to_camera()

        if camera_use:
            for i in range(1, len(coords)):
                xv,yv = self.create_vector(coords[i-1], coords[i], camera=True)
                for idx in range(len(xv)):
                    self.move_abs(x=xv[idx],y=yv[idx], f=self.speed_fast)
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

            
    




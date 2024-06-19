# Base imports
import os
import sys
import yaml
import argparse
import time
import numpy as np

# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\src'))

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

from system.cprinter import CPrinter
import cv2

staging = ""

def init_aero():
    global staging
    # Initialize stages using Aerotech class
    staging = Aerotech(stage_cfg['substrate']['GLASS'], incremental = False)
    staging.send_message('~INITQUEUE\n') # Initialize the queue



current_location = {
    "x":0,
    "y":0,
    "z":0
}

nozzle_position = {
    "x":0,
    "y":0,
    "z":0
}

safe_height = 18
speed_print = .27
speed_fast = 50
speed_slow = 0.5
speed_camera = 5

nozzle_now = True

base_camera_offset = system_cfg['camera_offset']

def set_pressure(pressure):
    """
    Set pressure of the system by taking input PSI
    and converting that to voltage using provided
    pressure model in pressure.yaml

    Parameters:
        pressure (float)    :    Pressure to set (PSI)
    """
    voltage = pressure_cfg['params']['gain'] * pressure + pressure_cfg['params']['bias']

    if voltage < 0.1:
        voltage = 0
        staging.set_pressure(voltage)
        current_pressure = 0
    elif voltage > 5:
        voltage = 5
        staging.set_pressure(voltage)
        current_pressure = (voltage - pressure_cfg['params']['bias']) / pressure_cfg['params']['gain']
    else:
        staging.set_pressure(voltage)
        current_pressure = pressure

def move_abs(x = None, y = None, z = None, f = .4):
    global current_location
    global nozzle_position

    if x is not None:
        current_location["x"] = x
    if y is not None:
        current_location["y"] = y
    if z is not None: 
        current_location["z"] = z
    
    staging.goto(x = x, y = y, z = z, f = f)

    if nozzle_now: 
        nozzle_position = current_location



def move_to_camera():
    """
    Method to move to camera based on the camera offset.

    """
    global current_location
    global nozzle_position
    global nozzle_now

    if nozzle_now:
        # Ensure pressure is off
        set_pressure(0)

        # Copy Nozzle Location
        nozzle_position = current_location.copy() 
        # Move in absolute so safe movement height 
        move_abs(z = safe_height, f = speed_fast)


        # Move to camera space
        move_abs(x = base_camera_offset[0]+nozzle_position["x"], y = base_camera_offset[1]+nozzle_position["y"], f = speed_fast)
        move_abs(z = base_camera_offset[1]+4, f = speed_fast)
        move_abs(z = base_camera_offset[2]+nozzle_position["z"], f = speed_camera)

        # Wait a bit
        time.sleep(2)

        # Set to current camera
        nozzle_now = False
    


def move_to_nozzle():
    """
    Method to move to camera based on the camera offset.

    """
    global current_location
    global nozzle_position
    global nozzle_now
    
    if not nozzle_now:
        # Ensure pressure is off
        set_pressure(0) 

        # Move in absolute so safe movement height 
        move_abs(z = safe_height, f = speed_fast)

        print(type(nozzle_position["z"]))
        print(type(base_camera_offset[2]))
        x = (nozzle_position["x"])
        y = (nozzle_position["y"])
        z = (nozzle_position["z"])

        print(f"x = {x}, y = {y}, z = {z}, f = {speed_fast}")

        # Move to nozzle space
        move_abs(x = nozzle_position["x"], y = nozzle_position["y"], f = speed_fast)
        move_abs(z = 4, f = speed_fast)
        move_abs(z = nozzle_position["z"], f = speed_camera)

        # Wait a bit
        time.sleep(2)

        # Set to current nozzle
        nozzle_now = True


speed = .44
coords_sqr = [
    [0,0],
    [0,5],
    [-5,5],
    [-5,0],
    [0,0],
    ]

coords_tri = [
    [0,0],
    [-2.5,5],
    [2.5,5],
    [0,0],
    ]

#sleeps = np.array(list(range(1, 10)))

cprint = CPrinter()

#cprint.move_to_camera()
cprint.
#time.sleep(3)

# Known Nozzle location

# cprint.nozzle_position = {
#     "x":0,
#     "y":0,
#     "z":0
# }

cprint.move_to_nozzle()

#print(cprint.camera_params)

""" img = cprint.grab_image_pylon()

_, binary = cv2.threshold(img,  0.9 * 255, 255, cv2.THRESH_BINARY)

cv2.imshow('image',binary)
cv2.waitKey(0)

cprint.move_to_nozzle() """

# cprint.set_pressure(20)
# for i in range(1, len(coords)):
#     xv,yv = cprint.create_vector(coords[i-1], coords[i])
#     for idx in range(len(xv)):
#         #print(f"x={xv[idx]},y={yv[idx]}, f={speed_slow}")
#         cprint.move_abs(x=xv[idx],y=yv[idx], f=speed_slow)
# cprint.set_pressure(0)

# cprint.move_to_camera()

# def save_pict(image, label):
#     print("Saving Picture")
#     dir_name = 'data_temp'
#     data_path = os.path.join(root_path, dir_name)
#     os.makedirs(data_path, exist_ok=True)

#     t_str = time.strftime("%Y%m%d-%H%M%S")
#     img_str = label + "_" + t_str + ".png"
#     img_path = os.path.join(data_path, img_str)
#     cv2.imwrite(img_path, image)

# for i in range(1, len(coords)):
#     xv,yv = cprint.create_vector(coords[i-1], coords[i], camera=True)
#     for idx in range(len(xv)):
#         cprint.move_abs(x=xv[idx],y=yv[idx], f=speed_slow)
#         img = cprint.grab_image_pylon()
#         save_pict(img, "Original")
#         _, binary = cv2.threshold(img,  0.9 * 255, 255, cv2.THRESH_BINARY)
#         save_pict(binary, "Binary")

cprint.move_to_camera()

cprint.nozzle_position = {
     "x":-8,
     "y":-28,
     "z":0
}

cprint.move_to_nozzle()
cprint.set_zero()

cprint.print_and_capture(coords_tri, 18)

cprint.move_to_camera()

cprint.nozzle_position = {
     "x":0,
     "y":8,
     "z":0
}

cprint.move_to_nozzle()
cprint.set_zero()

cprint.print_and_capture(coords_sqr, 18)
"""
for i in range(1, len(coords)):
    temp = cprint.dist_ang_calc(coords[i-1], coords[i])
    print(f"The distance between {coords[i-1]} and {coords[i]} in mm is {temp}")


print(f"testing: {np.linspace(0,0,100)}")
"""
"""
for s in sleeps:
    set_pressure(0)
    move_abs(z=safe_height, f=speed_fast)
    xmove = current_location["x"]+2
    move_abs(x=xmove, f=speed_fast)
    move_abs(z=2, f=speed_fast)
    time.sleep(5)
    move_abs(z=0, f=speed_slow)
    time.sleep(10)
    set_pressure(18)
    time.sleep(s)
    set_pressure(0)
    move_abs(z=safe_height, f=speed_fast)
"""




#set_pressure(18)
# for i in range(1, len(coords)+1):
#     listx = np.linspace(coords[i-1][0],coords[i][0],100)
#     listy = np.linspace(coords[i-1][1],coords[i][1],100)
#     for idx in range(len(listx)):
#         print(f"x = {listx[idx]}, y = {listy[idx]}")
#         move_abs(x = listx[idx], y = listy[idx], f=speed)
#time.sleep(2.0)
#set_pressure(0) 
#move_abs(z = safe_height, f = speed_fast)
#print(current_location["x"]+2)
""" # Set pressure from argument
set_pressure(18)
move_abs(x = 0, y = -2.5, f=speed)
set_pressure(14)
set_pressure(16)
set_pressure(18)
move_abs(x = 0, y = -5, f=speed/2)
set_pressure(20)
move_abs(x = 0, y = -5, f=speed*2)
move_abs(x = 2.5, y = -5, f=speed)
move_abs(x = 5, y = -5, f=speed/2)
move_abs(x = 5, y = -2.5, f=speed)
move_abs(x = 5, y = 0, f=speed/2)
move_abs(x = 2.5, y = 0, f=speed)
move_abs(x = 0, y = 0, f=speed/2)
#move_abs(x = 0, y = 0, f=.44)
move_abs(x = 0, y = 0, f=.44)

# Set pressure from argument
set_pressure(0) """
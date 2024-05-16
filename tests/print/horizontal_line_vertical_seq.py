#!/usr/bin/env python 

import os
import sys
import yaml
import argparser

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..\src'))
print(root_path)

sys.path.insert(0, root_path)

from system.printer import Printer
from vision.camera import Camera
from vision.line_width_estimator import LineWidthEstimator

# Create the parser
parser = argparse.ArgumentParser(description="Pressure value parser")

# Add required flag for pressure
parser.add_argument('--displacement', type=float, required=True, help='Direction and length of traversal')
parser.add_argument('--pressure', type=int, required=True, help='Pressure while printing')

# Parse the arguments
args = parser.parse_args()

print(args)

# Print receipe
update_print_location = [ [ 0, 0, 0],
                              [ -1.5, 0, 0],
                              [ -2.5, 0, 0], 
                              [ -3.5, 0, 0],
                              [ -4.5, 0, 0],
                              [ -5.5, 0, 0],
                              [ -6.5, 0, 0],
                              [ -7.5, 0, 0], 
                              [ -8.5, 0, 0] ]

# Take input arguements from user
displacement = args.displacement
printer = Printer()
speed = printer.base_speed
cam = Camera()
cam.run_camera()


# Activate pressure (regulator + solenoid)
printer.staging.set_pressure_regulator(1)
printer.set_pressure(args.pressure)
printer.staging.set_pressure_solenoid(1)

cnt = 0
for location in update_print_location:
    # Print single line
    printer.linear_b(0.1, 5)
    printer.linear(1, displacement, speed)
    printer.linear_b(-0.1, 5)

    # Update camera offset and move to camera
    printer.camera_offset[1] = abs(displacement) + printer.base_camera_offset[1]
    printer.camera_offset[0] = update_print_location[cnt][0] + printer.base_camera_offset[0]
    printer.move_to_camera()

    # Set interval to take images
    intervals = [(abs(displacement)/2.5), (abs(displacement)/15), (abs(displacement)/15)]
    line_widths = []
    updated_line_width = 0

    # Take three images and extract average line width
    for it in range(0, 3):
        printer.staging.goto(y=intervals[it], f=speed)
        captured_img = cam.grab_image()
        estimator =  LineWidthEstimator(captured_img)
        binary, contour = estimator.contour_detection()
        angle = estimator.get_orientation(contour)
        rot_image = estimator.rotate_image(contour, -angle)
        points, _, line_image = estimator.line_extraction(rot_image)
        line_width = estimator.line_width(points, printer.controller.ref_line_width)f
        line_widths.append(line_width)
        cnt+=1
    
    if len(line_widths) != 0:
        updated_line_width = sum(line_widths) / len(line_widths)

    printer.current_location = [printer.staging.x, printer.staging.y, printer.staging.z]

    printer.print_location = update_print_location[cnt+1]

    # Move back to nozzle
    printer.move_to_nozzle()

    # Update speed with process model
    speed, width_error = printer.update_process_model(updated_line_width, speed )
    
    # Increment counter
    cnt += 1





# Turn of pressure
printer.set_pressure(0)
#printer.staging.set_pressure_regulator(0)
#printer.staging.set_pressure_solenoid(0)


    




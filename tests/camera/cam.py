#!/usr/bin/env python

import cv2
import os
import sys
import yaml
import argparse
import time

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..\src'))
print(root_path)

sys.path.insert(0, root_path)

from vision.camera_controller import CameraController
from vision.image_grabber import ImageGrabber

# Create instance of CameraController Class 
camera_controller = CameraController("measurement_camera")

# Configure camera for software trigger
camera_controller.configure_for_software_trigger()

# Create instance of ImageGrabber Class    
image_grabber = ImageGrabber(camera_controller)
    

while True:
   # Grab a single image
    image = image_grabber.grab_image()

   # Show captured image  
    cv2.imshow('Measurement Camera', image)

    # Check for keyboard interrupt (press 'q' to quit)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


camera_controller.stop_grabbing()
camera_controller.close()
    
cv2.destroyAllWindows()


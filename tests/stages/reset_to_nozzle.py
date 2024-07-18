# Base imports
import os
import sys
import yaml

# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..\src'))

# Join root pathr
sys.path.insert(0, root_path)

from system.cprinter import CPrinter
import cv2

cprint = CPrinter()

cprint.move_to_camera()

cprint.move_to_nozzle()
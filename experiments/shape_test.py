# Base imports
import os
import sys
import yaml
import numpy as np

# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\src'))

# Join root path
sys.path.insert(0, root_path)

from system.cprinter import CPrinter
from vision.euclidean_width_estimator import EuclideanWidthEstimator

# Setup Printer
cprint = CPrinter()
cprint.nozzle_now = False

# Shapes
square = [[0,0], [-5,0], [-5, 5], [0, 5], [0, 0]]

# Job point
start_point = [0, 55]
cprint.load_next_job(start_point)

# Set Shape relative to start location
relative_square = cprint.update_relative_points(square, start_point)

job = "Test2"

# Print and Capture images
cprint.print_and_capture(relative_square, 18, job, camera_use = True)

ewe = EuclideanWidthEstimator()

ewe.process_job(job)


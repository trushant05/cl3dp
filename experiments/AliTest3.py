# Base imports
import os
import sys
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

# Experimental Setup
# Shapes
line = [[0,0], [0,10]]

calibration_line = [[0,0], [-10,0]]

cprint.print_and_capture(calibration_line, 20, .35, "Calibration", discrete=False, camera_use = False)

# EXPERIMENT 3
# Job point
start_points = [
                [0, 3],
                [-3, 3],
                [-6, 3],
                [-9, 3],
                [-12, 3],
]

pressures = [14, 16, 18, 20, 22]
speeds = [.21, .28, .35, .42, .49]
idx = 0

ewe = EuclideanWidthEstimator()

# Set Job Name
job = f"AliExp3-line-{idx}" 

for p in start_points:
    # Load Job
    cprint.load_next_job(p)
    # Set Shape relative to start location
    relative_square = cprint.update_relative_points(line, p)

    # Print and Capture images
    cprint.print_and_capture(relative_square, [pressures[2]], [speeds[idx]], job, camera_use = True)
    idx = idx + 1 
    job = f"AliExp3-line-{idx}" 

# Estimate Line Width
ewe.process_job(job)


# EXPERIMENT 4
# Job point
start_points = [
                [0, 18],
                [-3, 18],
                [-6, 18],
                [-9, 18],
                [-12, 18],
]

idx = 0
# Set Job Name
job = f"AliExp4-line-{idx}" 

for p in start_points:
    # Load Job
    cprint.load_next_job(p)
    # Set Shape relative to start location
    relative_square = cprint.update_relative_points(line, p)

    # Print and Capture images
    cprint.print_and_capture(relative_square, [pressures[idx]], [speeds[2]], job, camera_use = True)
    idx = idx + 1 
    job = f"AliExp4-line-{idx}" 

# EXPERIMENT 5
# Job point
start_points = [
                [0, 33],
                [-3, 33],
                [-6, 33],
                [-9, 33],
                [-12, 33],
]

idx = 0
# Set Job Name
job = f"AliExp5-line-{idx}" 

for p in start_points:
    # Load Job
    cprint.load_next_job(p)
    # Set Shape relative to start location
    relative_square = cprint.update_relative_points(line, p)

    # Print and Capture images
    cprint.print_and_capture(relative_square, [pressures[idx]], speeds, job, camera_use = True)
    idx = idx + 1 
    job = f"AliExp5-line-{idx}" 

# EXPERIMENT 6
# Job point
start_points = [
                [0, 48],
                [-3, 48],
                [-6, 48],
                [-9, 48],
                [-12, 48],
]

idx = 0
# Set Job Name
job = f"AliExp6-line-{idx}" 

for p in start_points:
    # Load Job
    cprint.load_next_job(p)
    # Set Shape relative to start location
    relative_square = cprint.update_relative_points(line, p)

    # Print and Capture images
    cprint.print_and_capture(relative_square, pressures, [speeds[idx]], job, camera_use = True)
    idx = idx + 1 
    job = f"AliExp6-line-{idx}" 
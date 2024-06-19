# Base imports
import os
import sys
import yaml
import numpy as np

# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\src'))

# Join root pathr
sys.path.insert(0, root_path)

from system.cprinter import CPrinter
import cv2

coords_line1 = [
    [0, 0],
    [-10, 0]
]

coords_line2 = [
    [0, 5],
    [-10, 5]
]

coords_line3 = [
    [0, 10],
    [-10, 10]
]

dot_start = [
    [0, 15]
]

dot_spacing = [
    [0, 5]
]

sleeps = np.array(list(range(1, 7)))

cprint = CPrinter()

cprint.nozzle_now = False

# Calibration and Clearing
cprint.print_and_capture(coords_line1, 20, "clearing", camera_use = False)

# Load Next Job
cprint.load_next_job(coords_line2[0])

# Calibration and Clearing
cprint.print_and_capture(coords_line2, 16, "16PSI")

# Load Next Job
cprint.load_next_job(coords_line3[0])

# Calibration and Clearing
cprint.print_and_capture(coords_line3, 18, "18PSI")

# Load Next Job
cprint.load_next_job(dot_start[0])

# Load Next Job
cprint.print_dots(sleeps, dot_spacing)



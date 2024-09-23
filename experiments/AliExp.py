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
    [-10, 0],
    [3, 0]
]

coords_line2 = [
    [-10, 10],
    [3, 10]
]

coords_line3 = [
    [-10, 15],
    [3, 15]
]

coords_line4 = [
    [-10, 20],
    [3, 20]
]

dot_start = [
    [-3, 25]
]

dot_spacing = [
    [0, 5]
]



sleeps = np.array(list(range(7, 11)))

cprint = CPrinter()

cprint.nozzle_now = False

# Load Next Job
cprint.load_next_job(coords_line1[0])

# Calibration and Clearing
line1_form = cprint.create_print_formula(coords_line1, [18], [.35], discrete = True)
#cprint.print_and_capture(line1_form, "clearing", camera_use = True)

# Load Next Job
cprint.load_next_job(coords_line2[0])

# Line 1
line1_form = cprint.create_print_formula(coords_line2, [30], [.5], discrete = True)
#cprint.print_and_capture(line1_form, "30PSI_0D5", camera_use = True)

# Load Next Job
cprint.load_next_job(coords_line3[0])

# Line 2
line1_form = cprint.create_print_formula(coords_line3, [30], [.75], discrete = True)
#cprint.print_and_capture(line1_form, "30PSI_0D75", camera_use = True)

# Load Next Job
cprint.load_next_job(coords_line4[0])

# Line 2
line1_form = cprint.create_print_formula(coords_line4, [40], [.50], discrete = True)
#cprint.print_and_capture(line1_form, "40PSI_0D50", camera_use = True)

# Load Next Job
cprint.load_next_job(dot_start[0])

# Load Next Job
cprint.print_dots(sleeps, dot_spacing)



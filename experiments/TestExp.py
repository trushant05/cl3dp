# Base imports
import os
import sys
import numpy as np

# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\src'))

# Join root path
sys.path.insert(0, root_path)

from jobs.job_loader import JobLoader

# Experimental Setup
# Shapes
start = [0,0]
line = [[0,0], [0,10]]
inv_line = [[0,0], [-10,0]]
pressures = [14, 15, 16, 17, 18, 19, 20]
#speeds = [.21, .28, .35, .42, .49, .56]
speeds = [.70] * len(pressures)
offset = 2
cols = 5

base_label = "pressure_test"

jl = JobLoader()

jl.load_job(start, inv_line, [18], [.35], "Calibration", camera_use = False, measure = False)

start = [0, offset]

for i in range(cols):
    base_label = f"base_label_column_{i}_row"
    jl.load_stacked_jobs(start, len(pressures), -1*offset, line, pressures, speeds, base_label, xstack = True, camera_use = True, measure = True)
    start[1] = start[1] + 10 + offset
    for i in range(len(pressures)):
        pressures[i] = pressures[i] + len(pressures)

jl.run_jobs()
# Base imports
import os
import sys
import numpy as np
from queue import Queue
import csv


# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

# Join root path
sys.path.insert(0, root_path)

from system.cprinter import CPrinter
from vision.euclidean_width_estimator import EuclideanWidthEstimator
from jobs.job import Job



class JobLoader:
    """
    A class for loading jobs into the cprinter.
    """

    def __init__(self):
        """
        Initializes a new instance of Printer class.
        """
        self.jobs = Queue(maxsize = 50)

        # Setup Printer
        self.cprint = CPrinter()
        self.cprint.nozzle_now = False

        # Setup Estimator
        self.ewe = EuclideanWidthEstimator()


    def load_job(self, start, points, pressures, speeds, label, camera_use = True, measure = True):
        # Load Job
        temp_job = Job(start, points, pressures, speeds, label, camera_use, measure=measure)
        self.jobs.put(temp_job)

    def load_stacked_jobs(self, start, stacks, offset, repeated_obj, pressure_per, speed_per, base_label, xstack = True, camera_use = True, measure = True):
        
        max_value = self.get_max_previous_stack(repeated_obj, x_direction = xstack)
        
        for i in range(stacks):
            temp_start = start.copy()
            if xstack:
                temp_start[0] = i*(max_value + offset)
            else:
                temp_start[1] = i*(max_value + offset)
            
            print(f"iter:{i}, temp_start:{temp_start}")

            temp_label = f"{base_label}_{i}"

            self.load_job(temp_start, repeated_obj, [pressure_per[i]], [speed_per[i]], temp_label, camera_use=camera_use, measure=measure)

    def get_max_previous_stack(self, repeated_obj, x_direction = False):

        max_value = 0

        # iterate per object
        for x, y in repeated_obj:
            print(f"x:{x},y:{y}")
            if x_direction:
                if x < max_value:
                    max_value = x
            else:
                if y > max_value:
                    max_value = y

        return max_value

    def run_jobs(self):

        results = []
        agg_results = os.path.join(self.ewe.data_path, "agg_results.csv" )
        
        while not self.jobs.empty():
            # Get Next Job
            current_job=self.jobs.get()
            job_listing = current_job.show_string()

            # Set Shape relative to start location
            relative_points = self.cprint.update_relative_points(current_job.points, current_job.start)

            # Load Job
            self.cprint.load_next_job(current_job.start)

            # Print and Capture images
            self.cprint.print_and_capture(relative_points, current_job.pressures, current_job.speeds, current_job.label, camera_use = current_job.camera_use)

            if current_job.measure:
                # Estimate Line Width
                results.extend(self.ewe.process_job(current_job.label, job_listing=job_listing))

        if len(results) > 0:
            with open(agg_results, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for res in results:
                    writer.writerow(res)







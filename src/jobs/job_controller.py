# Base imports
import os
import sys
import numpy as np
import pandas as pd


# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

# Join root pathr
sys.path.insert(0, root_path)

from jobs.job_loader import JobLoader
from jobs.job import Job
from control.controller import Controller

class JobController:
    """
    A class for controlling jobs into the cprinter.
    """

    def __init__(self, ref_line_width):
        """
        Initializes a new instance of Job Controller class.
        """
        self.jl = JobLoader()
        self.ct = Controller(ref_line_width)
        self.job_list = []
        self.possible_starts=[[0,0],[-12,0],[0,32],[-12,32]] 
        #self.possible_starts=[[0,32],[-12,32]] 
        self.jl.relative_start = self.possible_starts[0]
        self.res_columns = ['x', 'y', 'speed', 'pressure', 'img', 'job', 'last_measured']

    def add_job(self, start, points, pressures, speeds, label, controlled = False):
        # create Job
        temp_job = Job(start, points, pressures, speeds, label, controlled, measure=controlled, controlled=controlled)
        self.job_list.append(temp_job)

    def run_iteratively(self):

        df_results = ''

        idx = 0
        for ps in self.possible_starts:
            self.jl.relative_start = ps

            for j in self.job_list:
                if idx == 0:
                    j.label = f'{idx}-{j.label}'
                else:
                    j.label = str(idx) + j.label[1:]
                self.jl.import_job(j)
            
            testing_data=self.jl.run_jobs()
            print(testing_data)
            df_temp = ''

            if len(testing_data) > 0:
                df_temp = self.update_speeds(testing_data, idx)

            if len(df_results) < 1 :
                df_results = df_temp
            else:
                df_results = pd.concat([df_results, df_temp], ignore_index = True)
            idx = idx + 1

        return df_results


    def update_speeds(self, testing_data, idx):
        print(testing_data)
        print(idx)
        print(self.res_columns )

        df_temp = pd.DataFrame(data=testing_data, columns=self.res_columns)
        df_temp["iteration"] = [idx]*len(testing_data)

        df_temp['last_measured'] = df_temp['last_measured'].astype('float')
        df_temp['speed'] = df_temp['speed'].astype('float')

        print(df_temp.head())

        for j in self.job_list:
            print(j.show_string())
            if j.controlled:
                updates = df_temp[df_temp['job']==j.label]
                speeds = []
                for row in updates.iterrows():
                    speeds.append(self.ct.process_model(int(row[1][6]), row[1][2]))
                print(speeds)
                speeds = np.array(speeds)
                print(speeds[:,0])
                j.speeds = speeds[:,0]

        return df_temp



                


                







            
                 

    
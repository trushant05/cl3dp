import diplib as dip 
import numpy as np
import scipy
import glob
import os
import matplotlib.pyplot as plt
#from matplotlib_scalebar.scalebar import ScaleBar
import csv

# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class EuclideanWidthEstimator():
    def __init__(self):
        """
        Initializes a new instance of the Euclidean Width Estimator class.
        """
        self.data_folder = "data_temp"
        self.data_path = os.path.join(root_path, self.data_folder )

    def find_binary_png_files(self, job_path):
        pattern = job_path + '.\Binary\Binary*.png'
        binary_png_files = glob.glob(pattern)
        return binary_png_files

    def get_folders(self, directory):
        folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
        return folders

    def threshold_and_transform(self, image_path, save_path, save_img = False):
        # Get Image
        image = dip.ImageRead(image_path)
        # Threshold to black and white›
        imgt = image > 128
        # Generate Distance Transformation
        dt = dip.EuclideanDistanceTransform(imgt)

        if save_img:
            # Create Distance Transform Plots
            temp_name = save_path + "_dt.png"
            plt.title("Distance Transformation")
            plt.xlabel('X-Pixels')
            plt.ylabel('Y-Pixels')
            plt.imshow(dt)
            plt.savefig(temp_name)

        return dt

    def bounded_threshold(self, dist_transform, save_path, percent=.15, save_img = False):
        # Change to np array
        arr = np.array(dist_transform)

        # Gather the Maxima
        local_max = np.max(dist_transform)

        # Create dynamic threshold
        #thresh = desired - (max - desired)*1.1
        #thresh = local_max/2
        thresh = local_max*(1-percent)

        # Create new dist transformation minima binary
        dt2_b = dist_transform > thresh

        if save_img:
            # Create Local Maximum Bounding Plots
            temp_name = save_path + "_Max_Bounding.png"
            plt.title("Local Maximum Bounding")
            plt.xlabel('X-Pixels')
            plt.ylabel('Y-Pixels')
            plt.imshow(dt2_b)
            plt.savefig(temp_name)

        return dt2_b

    def skeleton_pathing(self, bounded_threshold, dist_transform, save_path, save_img = False):
        # Generate Skeleton
        sk = dip.EuclideanSkeleton(bounded_threshold)
        # Set Distance Transform to Array
        arr = np.asarray(dist_transform)
        # Gather non-zero values
        i = np.nonzero(sk)
        # Follow the skeleton line for values
        res = np.vstack([i, arr[i]])
        # Create Measurement
        res[2,:] = res[2,:]*2*1.52

        if save_img:
            # Create Skeleton Plots
            temp_name = save_path + "_Skeleton.png"
            plt.title("Skeleton")
            plt.xlabel('X-Pixels')
            plt.ylabel('Y-Pixels')
            plt.imshow(sk)
            plt.savefig(temp_name)

        return res

    def process_job(self, job, save_img=False, job_listing="Job Not Listed"):

        # Set job directory
        job_directory = os.path.join(self.data_path, job)

        # Get pictures in job directory
        pictures = self.find_binary_png_files(job_directory)

        # Make results directory
        results_directory = os.path.join(job_directory, "Results")
        os.makedirs(results_directory, exist_ok=True)

        results_csv = "results.csv"
        results_csv = os.path.join(results_directory, results_csv)

        temp_results = [["picture_timestamp", "job", "avg_width"]]

        for pict in pictures:
            # split off name
            temp = pict.split("Binary_")
            save_path = os.path.join(results_directory, temp[1][:-4])

            # create distance transform
            dt = self.threshold_and_transform(pict, save_path, save_img = save_img)

            # create distance transform
            b_th = self.bounded_threshold(dt, save_path, percent=.2, save_img = save_img)

            # use skeleton and create measurement
            measure_array = self.skeleton_pathing(b_th, dt, save_path, save_img = save_img)

            avg_measure = np.mean(measure_array[2,:])

            temp_results.append([temp[1][:-4], job, avg_measure])

        listing_path = os.path.join(results_directory, "job_listing.txt")
        f = open(listing_path, "w")
        f.write(job_listing)
        f.close()

        with open(results_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for res in temp_results:
                writer.writerow(res)

        return temp_results








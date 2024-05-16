# Import python modules
import cv2
import numpy as np
from scipy.signal import medfilt2d
from scipy.cluster.hierarchy import fclusterdata
import yaml
import time
import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.join(root_path, '..\config\camera.yaml')
sys.path.insert(0, root_path)

print(root_path)
print(config_path)

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

class LineWidthEstimator():
    """
    TODO
    """

    def __init__(self, image):
        self.px_mm_factor = config['params']['px_mm']
        self.threshold = 0.9
        self.image = image


    def contour_detection(self):
        _, binary = cv2.threshold(self.image, self.threshold * 255, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(binary.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour_image = np.zeros((binary.shape[0], binary.shape[1], 1), dtype=np.uint8)

        for itr, contour in enumerate(contours):
            color = [255, 255, 255]
            if len(contour) > 50:
                cv2.drawContours(contour_image, contours, itr, color, 1)

        return binary, contour_image

    def get_orientation(self, contour_image):
        line_img = contour_image.copy()
        lines = cv2.HoughLines(line_img, 1, np.pi/180, 200)

        angle_list = []
        try:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv2.line(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)
                angle_list.append(theta)

            max_theta = max(angle_list)
        except:
            max_theta = 0
        
        return max_theta

    def rotate_image(self, image, angle):
        (h, w) = image.shape[:2]
        (cx, cy) = (w // 2, h // 2)

        M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])

        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        M[0, 2] += (nW / 2) - cx
        M[1, 2] += (nH / 2) - cy

        return cv2.warpAffine(image, M, (nW, nH))

    def point_filter(self, val):

        input_array = np.array(val)

        # Reshape the array to a 2D array of (value, 0) pairs because fclusterdata expects a 2D array
        X = input_array.reshape(-1, 1)

        # Use fclusterdata to cluster the data, 1.5 is the threshold for clustering, method 'distance' means clustering based on the distance between points
        # The criterion 'distance' specifies that clusters are formed when the distances between points are below the threshold
        clusters = fclusterdata(X, 1.5, criterion='distance')

        # Find the mean of each cluster as the representative value
        cluster_means = [X[clusters == k].mean() for k in np.unique(clusters)]

        cluster_means_int = [int(round(X[clusters == k].mean())) for k in np.unique(clusters)]

        return cluster_means_int


    def line_extraction(self, contour_image):

        line_image = contour_image.copy()

        index_start = 100
        index_end = line_image.shape[1] - 101
    
        col_pts = np.linspace(index_start, index_end, 25, dtype=np.uint)
        points = {}
        for col in col_pts:
            lister = []
            for row in range(0, line_image.shape[0]):
                if (line_image[row][col] == 255):
                    lister.append(row)
            points[col] = lister

        for col, val in points.items():
            points[col] = self.point_filter(val)


        for col, val  in points.items():
            for row in val:
                coord = (col, row)
                cv2.circle(line_image, coord, 5, 255, -1)
            
        try:
            for col, val in points.items():
                cv2.line(line_image, (col, val[0]), (col, val[1]), 255, 3)

        except:
            print("No line to extract: Image might be dark")

        t_str = time.strftime("%Y%m%d-%H%M%S")
        img_str = "debug" + t_str + "test" + ".png"

        return points, contour_image, line_image


    def line_width(self, points, ref_line_width):
        dist = []
        for col, val in points.items():
            if len(points[col]) == 2:
                   line_width = abs(val[0] - val[1])
                   dist.append(line_width)

        if len(dist) != 0:
            avg_line_width = sum(dist) / len(dist)
        else:
            avg_line_width = 0
        return avg_line_width * self.px_mm_factor



    def show_image(self, image):
        while True:
            cv2.imshow('Output', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()



if __name__ == '__main__':
    pass
    #TODO




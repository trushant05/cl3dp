# Import python modules
import cv2
import numpy as np
from scipy.signal import medfilt2d
import time

base_path = 'C:\\Users\\trushant\\southern_research\\src'

class LineWidthEstimator():
    """
    TODO
    """

    def __init__(self, image):
        self.px_mm_factor = 1.52
        self.threshold_1 = 0.3
        self.threshold_2 = 0.6
        self.threshold_3 = 0.9

        self.image = image


    def contour_detection(self):
        _, binary_threshold_1 = cv2.threshold(self.image, self.threshold_1 * 255, 255, cv2.THRESH_BINARY)
        _, binary_threshold_2 = cv2.threshold(binary_threshold_1, self.threshold_2 * 255, 255, cv2.THRESH_BINARY)
        _, binary_threshold_3 = cv2.threshold(binary_threshold_2, self.threshold_3 * 255, 255, cv2.THRESH_BINARY)

        binary = binary_threshold_3.copy()

        contours, _ = cv2.findContours(binary.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contour_image = np.zeros((binary.shape[0], binary.shape[1], 3), dtype=np.uint8)

        for itr, contour in enumerate(contours):
            color = [255, 255, 255]
            if len(contour) > 50:
                cv2.drawContours(contour_image, contours, itr, color, 1)

        return contour_image


    def line_extraction(self, contour_image):

        line_image = cv2.cvtColor(contour_image, cv2.COLOR_BGR2GRAY)

        index_start = 100
        index_end = line_image.shape[1] - 101
    
        col_pts = np.linspace(index_start, index_end, 25, dtype=np.uint)
        points = {}
        for col in col_pts:
            lister = []
            for row in range(0, line_image.shape[0]):
                if (line_image[row][col] > 220):
                    lister.append(row)
            points[col] = lister


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
            if len(points[col]) <=2 and len(points[col]) > 1:
                   line_width = abs(val[0] - val[1])
                   dist.append(line_width)

        if len(dist) != 0:
            avg_line_width = sum(dist) / len(dist)
        else:
            avg_line_width = 0
        return avg_line_width



    def show_image(self, image):
        while True:
            cv2.imshow('Output', image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()



if __name__ == '__main__':
    pass
    #TODO




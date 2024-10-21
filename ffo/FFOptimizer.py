import numpy as np
import math
import os
import sys

# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Join root pathr
sys.path.insert(0, root_path)

from ffo.NLP import NLP_extrusion 
from ffo.smoothing_speed import *

class FeedforwardOptimizer:
    def __init__(self, params, s_max=.8e-3, s_min=0.01e-3, qq=15, ss=1, rr=0.001):
        """
        Initializes the FeedforwardOptimizer class with given parameters.
        
        :param params: Parameters for the optimization.
        :param s_max: Maximum speed limit.
        :param s_min: Minimum speed limit.
        :param Imax: Maximum iterations for optimization.
        :param qq, ss, rr: Coefficients for optimization calculations.
        """
        self.params = params
        self.s_max = s_max
        self.s_min = s_min
        self.qq = qq
        self.ss = ss
        self.rr = rr
    
    def set_coordinates(self, x_points, y_points, spr_ref, wpr_ref):
        """
        Sets the (x, y) coordinates and calculates speed control and dx.
        
        :param x_points: List or array of x coordinates.
        :param y_points: List or array of y coordinates.
        """
        self.x_points = np.array(x_points)
        self.y_points = np.array(y_points)

        self.wpr_ref = wpr_ref
        self.spr_ref = spr_ref

        self.Imax = len(x_points)
        
        self.P_pr_opt = np.zeros((self.Imax, 1))
        self.S_pr_opt = np.zeros((self.Imax, 1))
        self.W_pr_opt = np.zeros((self.Imax, 1))
        
        # Calculate angles and speed control
        self.angles = self.calculate_angles(self.x_points, self.y_points)
        self.speed_ctrl = self.calculate_speed_control(self.angles)
        
        # Calculate total distance and dx
        total_dist = self.total_distance(list(zip(self.x_points, self.y_points)))
        self.dx = total_dist / (self.Imax - 1)
    
    def optimize(self):
        """
        Runs the optimization process for given parameters.
        """
        extrusion_obj = NLP_extrusion(self.params, self.wpr_ref[0], self.spr_ref[0], 
                                      self.speed_ctrl[0], self.qq, self.ss, self.rr)

        for i in range(self.Imax):
            self.P_pr_opt[i], self.S_pr_opt[i], self.W_pr_opt[i] = extrusion_obj.optimize(
                self.params, self.wpr_ref[i], self.spr_ref[i], self.speed_ctrl[i], 
                self.qq, self.ss, self.rr)

        extrusion_obj.plotoptimal(self.wpr_ref, self.spr_ref, self.P_pr_opt, 
                                  self.S_pr_opt, self.W_pr_opt, self.speed_ctrl, 
                                  self.angles, 'non_smooth')

        # Smoothing the speed after 1st optimization
        angles_id, n_points_limits = Speed_changes_index(self.S_pr_opt)
        S_pr_opt_smt = speed_smooth_func(self.S_pr_opt, self.dx, angles_id, 
                                         n_points_limits, self.s_max, self.s_min, 6)
        plot_smooth_func(self.Imax, self.dx, self.S_pr_opt, S_pr_opt_smt)

        # Second round of optimization with smoothed speed
        self.P_pr_opt_smoothed = np.zeros((self.Imax, 1))
        self.S_pr_opt_smoothed = np.zeros((self.Imax, 1))
        self.W_pr_opt_smoothed = np.zeros((self.Imax, 1))
        spr_ref_new = S_pr_opt_smt

        extrusion_obj_smt = NLP_extrusion(self.params, self.wpr_ref[0], spr_ref_new[0], 
                                          self.speed_ctrl[0], self.qq, self.ss, 0)

        for i in range(self.Imax):
            self.P_pr_opt_smoothed[i], self.S_pr_opt_smoothed[i], self.W_pr_opt_smoothed[i] = extrusion_obj_smt.optimize(
                self.params, self.wpr_ref[i], spr_ref_new[i], self.speed_ctrl[i], 
                self.qq, self.ss, 0)

        extrusion_obj_smt.plotoptimal(self.wpr_ref, spr_ref_new, self.P_pr_opt_smoothed, 
                                      self.S_pr_opt_smoothed, self.W_pr_opt_smoothed, 
                                      self.speed_ctrl, self.angles, 'smoothed')

    def get_results(self):
        """
        Returns the optimized results.
        """
        return self.P_pr_opt_smoothed, self.S_pr_opt_smoothed, self.W_pr_opt_smoothed

    @staticmethod
    def calculate_speed_control(angles):
        """
        Static method to calculate speed control coefficients.
        
        :param angles: Angles between successive points in the printing pattern.
        :return: Speed control coefficients.
        """
        speed_ctrl = np.ones((angles.shape))
        for i in range(len(angles)):
            speed_ctrl[i] = np.exp((2 * np.log(150000) / np.pi) * angles[i]) if angles[i] <= np.pi/2 else 150000
        return speed_ctrl

    @staticmethod
    def calculate_angles(x_points, y_points):
        """
        Calculate angles between every set of three sequential points (vectors).
        
        :param x_points: List or array of x coordinates.
        :param y_points: List or array of y coordinates.
        :return: List of angles, padded with 0s at the beginning and end.
        """
        x_points = np.array(x_points)
        y_points = np.array(y_points)
        n = len(x_points)
        angles = np.zeros(n)

        for i in range(1, n - 1):
            v1 = np.array([x_points[i] - x_points[i - 1], y_points[i] - y_points[i - 1]])
            v2 = np.array([x_points[i + 1] - x_points[i], y_points[i + 1] - y_points[i]])
            v1_norm = v1 / np.linalg.norm(v1)
            v2_norm = v2 / np.linalg.norm(v2)
            angles[i] = np.arccos(np.clip(np.dot(v1_norm, v2_norm), -1.0, 1.0))

        return angles

    @staticmethod
    def total_distance(points):
        """
        Calculate the total distance traveled through a series of (x, y) points.
        
        :param points: List of (x, y) coordinates.
        :return: The total distance.
        """
        total_dist = 0.0
        for i in range(1, len(points)):
            x1, y1 = points[i-1]
            x2, y2 = points[i]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            total_dist += dist
        return total_dist

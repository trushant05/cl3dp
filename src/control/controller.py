import numpy as np
from sympy import symbols, diff
import os
import sys
import yaml

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.join(root_path, '..\config\controller.yaml')
sys.path.insert(0, root_path)

#print(root_path)
#print(config_path)

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)



class Controller:
    """
    Controller class with process model implementation.

    This class takes reference line width as input parameters and calculates
    stage speed based on the defined controller. 

    Attributes:
        ref_line_width  (float)   :  Input reference line width
        process_gain    (float)   :  Gain of the process
        process_bias    (float)   :  Bias of the process
        process_speed   (float)   :  Speed of the process
        C               (float)   :  Constant C
        learning_filter (float)   :  Learning filter of the process

    """

    def __init__(self, ref_line_width):
        """
        Initializes a new instance of Controller class.

        Parameters:
            ref_line_width (float)  :  Input reference line width

        """
        self.process_gain = config['params']['gain']
        self.process_bias = config['params']['bias']
        self.C = config['params']['C']

        self.ref_line_width = ref_line_width

        self.process_speed = 0.0
        self.learning_filter = 0.0


    def derivative_process_speed(self, line_width):
        """
        Evaluate derivative of the process model.

        Parameters:
            line_width (float)   :   Previous line width based on vision system

        """
        # Define the symbols
        line_width_sym, process_gain_sym, process_bias_sym = symbols('line_width process_gain process_bias')

        # Define the equation
        equation = (process_gain_sym / (line_width_sym + process_bias_sym))**2

        # Compute the derivative with respect to line_width
        derivative = diff(equation, line_width_sym)

        # Substitute the actual values
        derivative_evaluated = derivative.subs({
            line_width_sym: line_width,
            process_gain_sym: self.process_gain,
            process_bias_sym: self.process_bias
        })

        return derivative_evaluated


    def base_process(self, ref_line_width):
        """
        Method to evaluate initial stage speed based on ref_line_width.

        Parameters:
            ref_line_width (float)   :   Reference line width (expected)

        """
        speed = (self.process_gain / (ref_line_width + self.process_bias)) ** 2
        return speed


    def process_model(self, line_width, prev_speed):
        """
        Method to calcuate updated print_speed and width_error based
        on process model.

        Parameters:
            line_width (float)   :   Initial line width
            prev_speed (float)   :   Previous stage speed

        """
        derivative = self.derivative_process_speed(line_width)
        width_error = self.ref_line_width - line_width
        learning_filter = self.C * derivative
        self.learning_filter = learning_filter
        print_speed = prev_speed + (learning_filter * width_error)
        self.process_speed = print_speed

        return print_speed, width_error



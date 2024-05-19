#!/usr/bin/env python 

import os
import sys
import yaml
import argparser

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..\src'))
print(root_path)

sys.path.insert(0, root_path)

from system.printer import Printer

# Create the parser
parser = argparse.ArgumentParser(description="Pressure value parser")

# Add required flag for pressure
parser.add_argument('--displacement', type=float, required=True, help='Direction and length of traversal')
parser.add_argument('--speed', type=float, required=True, help='Speed of stage')
parser.add_argument('--pressure', type=int, required=True, help='Pressure while printing')

# Parse the arguments
args = parser.parse_args()

print(args)

# Fetch displacement direction and magnitude
displacement = args.displacement

# Fetch speed to move by
speed = args.speed

# Create instance of Printer() class
printer = Printer()

# Set pressure of the system
printer.set_pressure(args.pressure)

# Move in the given direction
printer.linear(0, displacement, speed)

# Set pressure to 0
printer.set_pressure(0)


    




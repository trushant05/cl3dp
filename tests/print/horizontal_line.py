#!/usr/bin/env python

import os
import sys
import yaml
import argparse

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

displacement = args.displacement

speed = args.speed

printer = Printer()

printer.staging.set_pressure_regulator(1)
printer.set_pressure(args.pressure)
printer.staging.set_pressure_solenoid(1)

printer.linear_b(0.1, 5)
printer.linear(1, displacement, speed)
printer.linear_b(-0.1, 5)

printer.set_pressure(0)
#printer.staging.set_pressure_regulator(0)
#printer.staging.set_pressure_solenoid(0)
    




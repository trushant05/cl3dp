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

# Parse the arguments
args = parser.parse_args()

print(args)

displacement = args.displacement

speed = args.speed

printer = Printer()

printer.linear_b(displacement, speed)
    




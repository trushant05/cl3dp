#!/usr/bin/env python

from time import sleep
import os
import sys
import yaml
import argparse

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..\src'))
stage_config_path = os.path.join(root_path, '..\config\stages.yaml')
pressure_config_path = os.path.join(root_path, '..\config\pressure.yaml')
sys.path.insert(0, root_path)

with open(stage_config_path, 'r') as file:
    stage_config = yaml.safe_load(file)

with open(pressure_config_path, 'r') as file:
    pressure_config = yaml.safe_load(file)

from stages.stage_control import Staging, Aerotech

print()
print('*' * 100)
print(root_path)
print(stage_config_path)
print(pressure_config_path)
print('*' * 100)
print()

print(stage_config)
print()

# Create the parser
parser = argparse.ArgumentParser(description="Pressure value parser")

# Add required flag for pressure
parser.add_argument('--pressure', type=int, required=False, help='Pressure as integer value (PSI)')
parser.add_argument('--enable', type=int, required=True, help='Enable 1 Disable 0')

# Parse the arguments
args = parser.parse_args()

aerotech_test = Aerotech(stage_config['substrate']['GLASS'], stage_config['mode']['incremental'])

def set_pressure(pressure):
    voltage = pressure_config['params']['gain'] * pressure + pressure_config['params']['bias']

    if voltage < 0.1:
        voltage = 0
        aerotech_test.set_pressure(voltage)
    elif voltage > 5:
        voltage = 5
        aerotech_test.set_pressure(voltage)
    else:
        aerotech_test.set_pressure(voltage)

aerotech_test.set_pressure_regulator(args.enable)
set_pressure(args.pressure)
aerotech_test.set_pressure_solenoid(args.enable)




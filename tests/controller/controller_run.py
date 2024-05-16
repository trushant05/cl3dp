#!/usr/bin/env python

import os
import sys
from time import sleep
import yaml

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..\src'))
config_path = os.path.join(root_path, '..\config\controller.yaml')
sys.path.insert(0, root_path)

from control.controller import Controller

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

print()
print('*' * 100)
print(root_path)
print(config_path)
print('*' * 100)
print()

print(config)
print()

control_test = Controller(config['params']['ref_line_width'])
speed = control_test.base_process(config['params']['ref_line_width'])
print(speed)




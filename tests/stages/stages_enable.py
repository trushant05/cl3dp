#!/usr/bin/env python

from time import sleep
import os
import sys
import yaml

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..\src'))
config_path = os.path.join(root_path, '..\config\stages.yaml')
sys.path.insert(0, root_path)

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

from stages.stage_control import Staging, Aerotech

print()
print('*' * 100)
print(root_path)
print(config_path)
print('*' * 100)
print()

print(config)
print()

aerotech_test = Aerotech(config['substrate']['GLASS'], config['mode']['incremental'])





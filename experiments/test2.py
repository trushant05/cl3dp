# Base imports
import os
import sys
import yaml
import argparse
import time
import numpy as np

# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\src'))
# Join root pathr
sys.path.insert(0, root_path)

# Import Aerotech and staging
from stages.stage_control import Staging, Aerotech

from system.cprinter import CPrinter
import cv2

cprint = CPrinter()

cprint.move_abs(z=18, f=cprint.speed_fast)
cprint.move_abs(x=97.7832, y=-5.4304, f=cprint.speed_fast)
cprint.move_abs(z=2, f=cprint.speed_fast)
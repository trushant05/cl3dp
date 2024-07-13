# Printer Overview

<p align="justify">Printer Class is the main class which will handle initialization of stages and controller. Images captured by camera interface will be pass to printer class. The location of this file is <b>src -> system -> printer.py</b> and the configuration file is <b>config -> printer.yaml</b> parameters to which are as follow:</p>

- axes:
    - x_axis:
        - id: 0
        - speed: 5
        - speed_fast: 50
    - y_axis:
        - id: 1
        - speed: 50
        - speed_fast: 50
    - z_axis:
        - id: 2
        - speed: 50
        - speed_slow: 0.5

- camera_offset:
    - -98.3159
    - 1.1260
    - 5.2599

- moving_height: 18

- recipe:
    - 0
    - 0
    - 0





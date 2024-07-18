# Printer Overview

<p align="justify">
Printer Class is the main class which will handle initialization of stages and controller. Images
captured by camera interface will be pass to printer class. The location of this file is <b> src 
-> system -> printer.py </b> and the configuration file is <b> config -> printer.yaml </b> parameters
to which are as follow:</p>

```yaml
# File -> printer.yaml

axes:
    - x_axis:
        - id: 0
        - speed: 5
        - speed_fast: 50
    - y_axis:
        - id: 1
        - speed: 5
        - speed_fast: 50
    - z_axis:
        - id: 2
        - speed: 50
        - speed_slow: 0.5

camera_offset:
    - -98.3159
    - 1.1260
    - 5.2599

moving_height: 18

 recipe:
    - 0
    - 0
    - 0

```

## Printer Test
<p align="justify">
Printer Class could be tested in two ways, one is to test movement without pressure and one with pressure.</p>

#### 1. Movement Test

<p align="justify">
In order to test the movement of the stages, three scripts corresponding to each stage is provided in <b> tests -> move </b> directory.</p>

```sh
Note: Use +/- ve with --displacement flag to change direction of movement
```

Move stages in x axis:
```sh 
python tests/move/x.py --displacement 10 --speed 1
```

Move stages in y axis:
```sh 
python tests/move/y.py --displacement 10 --speed 1
```

Move stages in z axis:
```sh 
python tests/move/z.py --displacement 2 --speed 0.5
```

#### 2. Print Test

<p align="justify">
In order to test the printing, two scripts are provided one of which prints vertically and other horizontally
in <b> tests -> print </b> directory.</p>

Print line horizontally:
```sh
python tests/print/horizontal_line.py --displacement 15 --speed 0.4 --pressure 10
```

Print line vertically:
```sh
python tests/print/vertical_line.py --displacement 15 --speed 0.4 --pressure 10
```
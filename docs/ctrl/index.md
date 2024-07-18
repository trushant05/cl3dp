# Controller Overview

<p align="justify">
A P-type controller is implemented in <b>src -> control -> controller.py</b> based on the reference
line width to output stage speed for achieving that line width. The configuration file containing
process model parameters resides in <b>config -> controller.yaml</b> which has following structure:</p>

```yaml
# File -> controller.yaml

params:
    - gain: 201.22
    - bias: 22.705
    - C: 0.2
    - ref_line_width: 280
```

## Controller Test 

<p align="justify">
In order to test if the controller is working as expected, we can run <b> tests -> controller -> controller_run.py </b>
file which takes reference line width as input parameter from <b> controller.yaml </b> config file to generate stage
speed to achieve that line width. </p>

```sh
python tests/controller/controller_run.py
```

<img src="/assets/img/ctrl/controller_test.png" alt="Controller Test" class="centered-image-medium">


<p align="justify">
For a given reference line widht of 280 microns, initial stage speed according to the controller is 0.44187 mm/s.
After a new line is printed at this speed, we will estimate line width using a vision system and that will serve as
input for next iteration. This process will go on till the controller converges (error is less than some delta). </p>
# Controller Overview

<p align="justify">A P-type controller is implemented in <b>src -> control -> controller.py</b> based on the reference line width to output stage speed for achieving that line width. The configuration file containing process model parameters resides in <b>config -> controller.yaml</b> which has following structure:</p>

- params:
    - gain: 201.22
    - bias: 22.705
    - C: 0.2
    - ref_line_wdith: 280

# Stages Overview

<p align="justify">
Codebase to control stages resides in <b>src -> stages -> stage_control.py</b> and the configuration file resides in
<b>config -> stages.yaml</b>. Make sure to configure <b>stages.yaml</b> according to system setup parameters to which 
are as follow: </p>

```yaml
# File -> stages.yaml

- connection:
    - PC_IP_ADDRESS: "xxx.xxx.xxx.xxx"
    - PORT: 8000
    - SOCKET_TIMEOUT: 600
- mode:
    - incremental: True
- substrate:
    - GLASS: 0
    - SILICON: 1
```

Note: There are some parameters for Safety Zone which will be implemented later.
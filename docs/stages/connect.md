# Stages Connection Setup

1. Extract IP address of current host computer attached to stages:
    - Open command prompt and use following command:

        ```sh
         ipconfig 
        ```

    <img src="/assets/img/stages/ip_fetch.png" alt="IP Fetch" class="centered-image-small">


    From the output use Ethernet adapter's IPv4 Address. Incase you are using WiFi adapter, use that IPv4 instead.

2. Get Port for ASCII server:
    - Open A3200 Configuration Manager and int he left pane go to following parameter:

        **config_file -> System -> Communication -> ASCII -> CommandPort**

    <img src="/assets/img/stages/port_fetch.png" alt="Port Fetch" class="centered-image-medium">

    Note: Keep all other parameters default for now.


## Stage Connection Test

<p align="justify">
In order to test if the connection with stages is established, we can run **test -> stages -> stages-enable.py** file
which will enable all three (X, Y and Z stage) by using following command: </p>
```sh
python tests/stages/stages_enable.py 
```

<img src="/assets/img/stages/stage_test.png" alt="Stage Test" class="centered-image-large">

The output states following:

- **Stages Enabled**: All three stages (X, Y, and Z) are enabled in incremental mode.
- **Unit System**: The system is using SI units (Metric, Second).
- **RAMP Rate**: The RAMP rate is set to 100.
- **Safezones**: All safezones are cleared.
- **Connection Status**: The Aerotech connection is closed after sending the commands.

You can verify these settings using the A3200 CNC Operator.

<img src="/assets/img/stages/stage_test_val.png" alt="Stage Test Validation" class="centered-image-medium">
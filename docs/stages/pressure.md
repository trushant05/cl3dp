# Pressure 

<p align="justify">The model to convert pressure in PSI to dedicated voltage will be implemented in the <b>printer.py</b> file. That voltage would then be passed to setPressure method in Aerotech Class declared in <b>stage_control.py</b>.</p>

Definition of the method is as follow:

![](./../assets/pressure_method.png)

<p align="justify">Two considerations to keep in mind, the pressure passed as argument to set_pressure method is corresponding voltages (not PSI) and it can be seen that the pressure circuit it attached to X stage controller.</p>

<p align="justify">The <b>pressure.yaml</b> configuration file contains gain and bias to convert either pressure (PSI) -> volatage or vice versa:</p>

- params:
    - gain: 0.0844
    - bias: 0.0899

```
voltage = gain * pressure + bias       # PSI -> V

pressure = (voltage - bias) / gain     # V -> PSI
```

### Test Pressure
<p align="justify">In order to test the pressure, we can run <b>tests -> stages -> pressure_test.py</b> using following command from root directory: (Pressure is passed as an argument in PSI along with regulator and solenoid enabler)</p>

```
python tests/stages/pressure_test.py --pressure 12 --enable 1 

python tests/stages/pressure_test.py --enable 0
```


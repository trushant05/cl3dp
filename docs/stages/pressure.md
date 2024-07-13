# Pressure to Voltage Mapping

<p align="justify">
The model to convert pressure in PSI to dedicated voltage will be impletement in <b>printer.py</b> file.
That voltage would then be passed to <i>setPressure</i> method in Aerotech Class declared in <b>stage_control.py</b>. </p>

```python
def set_pressure(self, pressure = None):
    """
    Method to set pressure of the system.

    Parameters:
        pressure (float) : Using the process model intended pressure is converted
                           to respective voltage.

    Note:
        Here analog pin0 on X stage is used which might not always be the case
    """
    if pressure != None:
        msg = '$AO[1].X = '
        msg += '%0.6f' %pressure
    else:
        raise ValueError('staging.setPressure() was called with all None arguments')
    msg += '\n'
    print(msg)
    self.send_message(msg)
```

<p align="justify">
Two considerations to keep in mind, the pressure passed as argument to <b>set_pressure</b> method
is corresponding voltage (not PSI) and it can be seen that the pressure circuit it attached in X
stage controller.</p>

<p align="justify">
The <b>pressure.yaml</b> configuration file contains gain and bias to convert either <b> pressure (PSI) -> voltage </b> or vica versa: </p>

```yaml
# File -> pressure.yaml

params:
    - gain: 0.0844
    - bias: 0.0899
```

```
voltage = gain * pressure + bias  # PSI ->  V
pressure = (voltage - bias) /gain # V   ->  PSI
```

## Pressure Test

<p align="justify">
In order to test the pressure, we can run <b> tests -> stages -> pressure_test.py </b> using following
command from root directory: (Pressure is passed as an argument in PSI along with regulator and
solenoid enabler) </p>

```sh
python tests/stages/pressure_test.py --pressure 12
python tests/stages/pressure_test.py --pressure 0
```
# Testing

<p align="justify">In order to test if the controller is working as expected, we can run <b>tests -> controller -> controller_run.py </b>file which takes reference line width as input parameter from <b>controller.yaml</b> config file to generate stage speed to achieve that line width.</p>

```
python tests/controller/controller_run.py
```

![](../assets/controller_test.png)

<p align="justify">For a given reference line width of 280 microns, intial stage speed according to the controller is 0.44187 mm/s. After a new line is printed at this speed, we will estimate line width using a vision system and that will serve as input for next iteration. This process will go on till the controller converges ( error is less than some delta ).</p>

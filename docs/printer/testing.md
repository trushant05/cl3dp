# Testing

<p>Printer class could be tested in two ways, one is to test movement without pressure and one with pressure.</p>

### Movement Test
<p align="justify">In order to test the movement of the stages, three scripts corresponding to each stage is provided in <b>tests -> move</b> directory.</p>

Move stages in x axis:

```
python tests/move/x.py --displacement 10 --speed 1
```

Move stages in y axis:

```
python tests/move/y.py --displacement 10 --speed 1
```

Move stages in z axis:

```
python tests/move/z.py --displacement 2 --speed 0.1
```

Move stages in b axis:

```
python tests/move/b.py --displacement 0.1 --speed 5
python tests/move/b.py --displacement -0.1 --speed 5
```

### Print Test
<p align="justify">In order to test the printing, two scripts are provided one of which prints vertically and other horizontally in <b>tests -> print</b> directory.</p>

Print line horizontally:

```
python tests/print/horizontal_line.py --displacement 15 --speed 0.4 --pressure 10
```

Print line vertically:

```
python tests/print/vertical_line.py --displacement 15 --speed 0.4 --pressure 10
```

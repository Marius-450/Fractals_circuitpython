# Fractals_circuitpython
Fractals drawing lib for circuitpython

## Intro

This lib is developped to demonstrate the capabilities of circuitpython, and to find the limits of the microcontrolers.

## Usage

simple example

```python
import fractals
import displayio
import board

display = board.DISPLAY
group = displayio.Group()
display.show(group)
group = fractals.mandelbrot(display.width, display.height, group=group)

while True:
    pass
```

## More infos

* Mandelbrot
  * [wikipedia](https://en.wikipedia.org/wiki/Mandelbrot_set)
  * [original code for pygamer board](https://lecluseo.scenari-community.org/CircuitPython/co/g_mandelbrot.html)
  
* 


## 


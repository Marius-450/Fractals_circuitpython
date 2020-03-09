import time
import board
import displayio
from random import randint

import fractals

display = board.DISPLAY

group = displayio.Group()
display.show(group)

group = fractals.mandelbrot(display.width, display.height, 127, group=group)
time.sleep(60)
while True:
    rand_point = fractals.mandelbrot_points[randint(0, len(fractals.mandelbrot_points)-1)]
    group = fractals.mandelbrot(display.width, display.height, 255, group, rand_point[0], rand_point[1])
    # 5 minutes pause.
    time.sleep(300)
    pass

import time
import board
import displayio
import fractals

display = board.DISPLAY

group = displayio.Group()
display.show(group)


while True:
    start = time.monotonic()
    group = fractals.quasicrystal(display.width, display.height, 16, group)
    print(time.monotonic()-start, "secs to draw")
    time.sleep(0.01)


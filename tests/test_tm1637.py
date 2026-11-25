"""Stand-alone test of the TM1637 display.

Upload config.py and tm1637.py to the Pico, then run this file.
"""
from time import sleep_ms
import config
from tm1637 import TM1637

display = TM1637(config.TM_CLK_PIN, config.TM_DIO_PIN, config.TM_BRIGHTNESS)

for n in (0, 7, 42, 123, 4000):
    print("number", n)
    display.show_number(n)
    sleep_ms(1000)

for v in (0.5, 10.0, 29.6, 45.6, 123.4):
    print("decimal", v)
    display.show_decimal(v, 1, colon=config.TM_COLON)
    sleep_ms(1000)

display.show_dashes()
sleep_ms(1000)
display.show_error()
sleep_ms(1000)

for b in range(8):
    display.brightness = b
    display.show_number(8888)
    sleep_ms(300)

display.clear()
print("done")

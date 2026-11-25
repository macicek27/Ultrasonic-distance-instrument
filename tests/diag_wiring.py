"""Wiring test of GP14 (Trig) and GP15 (Echo) - without the sensor.

Before running, put a jumper on the breadboard from B2 to F2
(connects the Trig row with the GP15 row). Remove it after the test!

Result:
  GP14=1 -> GP15 = 1  and  GP14=0 -> GP15 = 0   => wires are OK
  otherwise                                      => wire in a wrong pin / hole
"""
from machine import Pin
import time

trig = Pin(14, Pin.OUT, value=0)   # GP14
echo = Pin(15, Pin.IN)             # GP15

for i in range(3):
    trig.value(1)
    time.sleep_ms(50)
    print("GP14=1 -> GP15 =", echo.value())
    trig.value(0)
    time.sleep_ms(50)
    print("GP14=0 -> GP15 =", echo.value())

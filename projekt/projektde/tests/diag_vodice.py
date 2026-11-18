"""Test vodičů GP14 (Trig) a GP15 (Echo) - bez senzoru.

Před spuštěním dejte na nepájivé pole propojku z B2 do F2
(spojí řádek Trig s řádkem GP15). Po testu propojku zase vyndejte!

Výsledek:
  GP14=1 -> GP15 = 1  a  GP14=0 -> GP15 = 0   => vodiče jsou v pořádku
  jinak                                        => vodič je ve špatném pinu / dírce
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

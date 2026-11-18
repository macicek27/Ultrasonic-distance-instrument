"""Test displeje TM1637 samostatně.

Na Pico nahrajte config.py a tm1637.py, pak spusťte tento soubor.
"""
from time import sleep_ms
import config
from tm1637 import TM1637

display = TM1637(config.TM_CLK_PIN, config.TM_DIO_PIN, config.TM_BRIGHTNESS)

for n in (0, 7, 42, 123, 4000):
    print("cislo", n)
    display.show_number(n)
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
print("hotovo")

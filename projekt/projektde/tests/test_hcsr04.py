"""Test HC-SR04 samostatně.

Na Pico nahrajte config.py a hcsr04.py, pak spusťte tento soubor.
Vypíše 20 měření a jejich rozptyl (hodí se do kapitoly Testování).
"""
from time import sleep_ms
import config
from hcsr04 import HCSR04

sonar = HCSR04(config.TRIG_PIN, config.ECHO_PIN)
values = []

for i in range(20):
    cm = sonar.distance_cm()
    print(i, "---" if cm is None else "%.1f cm" % cm, sonar.status)
    if cm is not None:
        values.append(cm)
    sleep_ms(100)

if values:
    print("platnych: %d/20  min %.1f  max %.1f  prumer %.1f cm" % (
        len(values), min(values), max(values), sum(values) / len(values)))

"""Stand-alone test of the HC-SR04 sensor (raw values, no calibration).

Upload config.py and hcsr04.py to the Pico, then run this file.
Put a large flat obstacle (wall, board) at a known distance measured from the
front face of the sensor's metal cylinders and set SENSOR / REAL_CM below.
The result line is used for the calibration table in README.md.
"""
from time import sleep_ms
import config
from hcsr04 import HCSR04

SENSOR = "1"      # which sensor piece is tested (1 or 2)
REAL_CM = 30      # real distance measured with a ruler
SAMPLES = 30

sonar = HCSR04(config.TRIG_PIN, config.ECHO_PIN)   # scale=1, offset=0 -> raw values
values = []
pulses = []

for i in range(SAMPLES):
    cm = sonar.distance_cm()
    print(i, "---" if cm is None else "%.1f cm" % cm, sonar.last_pulse_us, "us", sonar.status)
    if cm is not None:
        values.append(cm)
        pulses.append(sonar.last_pulse_us)
    sleep_ms(100)

if values:
    mean = sum(values) / len(values)
    print("sensor %s  real %d cm  valid %d/%d  min %.1f  max %.1f  mean %.1f cm  (error %+.1f cm)  mean pulse %d us" % (
        SENSOR, REAL_CM, len(values), SAMPLES, min(values), max(values), mean,
        mean - REAL_CM, sum(pulses) // len(pulses)))
else:
    print("no valid measurement, status:", sonar.status)

"""HC-SR04 diagnostics - prints the raw ECHO pulse width.

Needs no other files. Run it with: right click in the code ->
MicroPico -> Run Current File on Board.

How to read the result:
  pulse 1000-3000 us  -> sensor works (1750 us is about 30 cm)
  pulse ~38000 us     -> no echo received (aim at a wall or a large board)
  idle 1 or pulse -1  -> ECHO is stuck high (wiring error)
  pulse -2            -> ECHO never arrived (wiring or power error)
"""
from machine import Pin, time_pulse_us
import time

trig = Pin(14, Pin.OUT, value=0)  # GP14
echo = Pin(15, Pin.IN)            # GP15 (via voltage divider)

for i in range(10):
    idle = echo.value()
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    pulse = time_pulse_us(echo, 1, 60000)
    if pulse > 0:
        print("echo idle:", idle, "  pulse:", pulse, "us  =", round(pulse * 0.0343 / 2, 1), "cm")
    else:
        print("echo idle:", idle, "  pulse:", pulse)
    time.sleep_ms(200)

"""Ultrasonic distance instrument - main program.

Three tasks run concurrently (asyncio):

* ``measure_task``  every 100 ms - measure distance, set LED and relay
* ``display_task``  every 200 ms - show the distance (1 decimal place) on the TM1637 display
* ``button_task``   every 20 ms  - button toggles HOLD (freezes the display)

``log_task`` prints the measured distance to the serial console once a second.
"""

try:
    import asyncio
except ImportError:  # older MicroPython firmware
    import uasyncio as asyncio

from machine import Pin

import config
from hcsr04 import HCSR04, STATUS_ERROR
from tm1637 import TM1637
from rgb_led import RgbLed, GREEN, PURPLE, RED, BLUE
from relay import Relay


class State:
    """Values shared between the tasks."""

    def __init__(self):
        self.distance = None    # distance in cm, None = invalid measurement
        self.status = STATUS_ERROR
        self.hold = False       # True = display keeps the last value


def update_outputs(state, led, relay):
    """Set the LED colour and the relay according to the distance."""
    d = state.distance
    if state.status == STATUS_ERROR:
        led.set(BLUE)               # sensor error
        relay.off()
    elif d is None or d >= config.FAR_CM:
        led.set(GREEN)              # far away or nothing in range
        relay.off()
    elif d >= config.NEAR_CM:
        led.set(PURPLE)             # getting closer (yellow was hard to see)
        relay.off()
    else:
        led.set(RED)                # too close -> relay on
        relay.on()


async def measure_task(sonar, state, led, relay):
    while True:
        # distance_cm() waits for ECHO at most ~30 ms, other tasks are delayed only briefly
        state.distance = sonar.distance_cm()
        state.status = sonar.status
        update_outputs(state, led, relay)
        await asyncio.sleep_ms(config.MEASURE_PERIOD_MS)


async def display_task(display, state):
    while True:
        if state.hold:
            pass                        # HOLD: keep the last value on the display
        elif state.status == STATUS_ERROR:
            display.show_error()
        elif state.distance is None:
            display.show_dashes()       # nothing in range
        else:
            # e.g. 29.6 cm -> "29:6" on our clock-type module (colon = decimal separator)
            display.show_decimal(state.distance, 1, colon=config.TM_COLON)
        await asyncio.sleep_ms(config.DISPLAY_PERIOD_MS)


async def button_task(button, state):
    last = 1
    while True:
        value = button.value()
        if value == 0 and last == 1:        # pressed (button connects to GND)
            state.hold = not state.hold
            print("HOLD on" if state.hold else "HOLD off")
        last = value
        await asyncio.sleep_ms(config.BUTTON_PERIOD_MS)


async def log_task(state):
    await asyncio.sleep_ms(500)  # wait for the first measurement
    while True:
        if state.distance is None:
            print("distance: ---  status:", state.status)
        else:
            print("distance: %.1f cm" % state.distance)
        await asyncio.sleep_ms(1000)


async def main():
    state = State()
    sonar = HCSR04(config.TRIG_PIN, config.ECHO_PIN,
                   scale=config.CAL_SCALE, offset_cm=config.CAL_OFFSET_CM)
    display = TM1637(config.TM_CLK_PIN, config.TM_DIO_PIN, config.TM_BRIGHTNESS)
    led = RgbLed(config.LED_R_PIN, config.LED_G_PIN, config.LED_B_PIN)
    relay = Relay(config.RELAY_PIN, config.RELAY_ACTIVE_LOW)
    button = Pin(config.BUTTON_PIN, Pin.IN, Pin.PULL_UP)

    asyncio.create_task(measure_task(sonar, state, led, relay))
    asyncio.create_task(display_task(display, state))
    asyncio.create_task(button_task(button, state))
    await log_task(state)


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()

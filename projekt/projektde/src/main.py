"""Ultrazvukový měřič vzdálenosti - hlavní program.

Běží 3 úlohy současně (asyncio):

* ``measure_task``  každých 100 ms  - změří vzdálenost, nastaví LED a relé
* ``display_task``  každých 200 ms  - zobrazí vzdálenost na TM1637
* ``button_task``   každých 20 ms   - tlačítko zapíná/vypíná HOLD (zmrazení displeje)
"""

try:
    import asyncio
except ImportError:  # starší firmware MicroPythonu
    import uasyncio as asyncio

from machine import Pin

import config
from hcsr04 import HCSR04, STATUS_ERROR
from tm1637 import TM1637
from rgb_led import RgbLed, GREEN, YELLOW, RED, BLUE
from relay import Relay


class State:
    """Hodnoty sdílené mezi úlohami."""

    def __init__(self):
        self.distance = None    # vzdálenost v cm, None = neplatné měření
        self.status = STATUS_ERROR
        self.hold = False       # True = displej drží poslední hodnotu


def update_outputs(state, led, relay):
    """Podle vzdálenosti nastaví barvu LED a relé."""
    d = state.distance
    if state.status == STATUS_ERROR:
        led.set(BLUE)               # chyba senzoru
        relay.off()
    elif d is None or d >= config.FAR_CM:
        led.set(GREEN)              # daleko nebo nic v dosahu
        relay.off()
    elif d >= config.NEAR_CM:
        led.set(YELLOW)             # blíží se
        relay.off()
    else:
        led.set(RED)                # moc blízko -> sepnout relé
        relay.on()


async def measure_task(sonar, state, led, relay):
    while True:
        # distance_cm() čeká na ECHO nejdéle ~30 ms, ostatní úlohy to nezdrží výrazně
        state.distance = sonar.distance_cm()
        state.status = sonar.status
        update_outputs(state, led, relay)
        await asyncio.sleep_ms(config.MEASURE_PERIOD_MS)


async def display_task(display, state):
    while True:
        if state.hold:
            pass                        # HOLD: displej nechá poslední hodnotu
        elif state.status == STATUS_ERROR:
            display.show_error()
        elif state.distance is None:
            display.show_dashes()       # nic v dosahu
        else:
            display.show_number(round(state.distance))
        await asyncio.sleep_ms(config.DISPLAY_PERIOD_MS)


async def button_task(button, state):
    last = 1
    while True:
        value = button.value()
        if value == 0 and last == 1:        # stisk (tlačítko spíná proti GND)
            state.hold = not state.hold
            print("HOLD" if state.hold else "mereni")
        last = value
        await asyncio.sleep_ms(config.BUTTON_PERIOD_MS)


async def log_task(state):
    await asyncio.sleep_ms(500)  # počkat na první měření
    while True:
        if state.distance is None:
            print("vzdalenost: ---  stav:", state.status)
        else:
            print("vzdalenost: %.1f cm" % state.distance)
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

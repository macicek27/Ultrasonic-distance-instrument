"""Třída pro RGB LED modul se společnou katodou (Iduino 3-color LED)."""

from machine import Pin

OFF = (0, 0, 0)
GREEN = (0, 1, 0)
YELLOW = (1, 1, 0)
RED = (1, 0, 0)
BLUE = (0, 0, 1)


class RgbLed:
    """RGB LED – každá barva má svůj GPIO pin. Rezistory jsou už na modulu.

    :param r: číslo GPIO pro červenou (pin R).
    :param g: číslo GPIO pro zelenou (pin G).
    :param b: číslo GPIO pro modrou (pin B). Pin ``-`` patří na GND.
    """

    def __init__(self, r, g, b):
        self.pins = (Pin(r, Pin.OUT, value=0), Pin(g, Pin.OUT, value=0), Pin(b, Pin.OUT, value=0))

    def set(self, color):
        """Nastaví barvu.

        :param color: trojice (r, g, b) z hodnot 0/1, např. ``rgb_led.GREEN``.
        """
        for pin, value in zip(self.pins, color):
            pin.value(value)

    def off(self):
        """Zhasne LED."""
        self.set(OFF)

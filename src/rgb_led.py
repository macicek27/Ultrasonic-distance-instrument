"""Driver class for an RGB LED module with a common cathode (Iduino 3-color LED)."""

from machine import Pin

OFF = (0, 0, 0)
GREEN = (0, 1, 0)
PURPLE = (1, 0, 1)
RED = (1, 0, 0)
BLUE = (0, 0, 1)


class RgbLed:
    """RGB LED - each colour has its own GPIO pin. Resistors are on the module.

    :param r: GPIO number for red (pin R).
    :param g: GPIO number for green (pin G).
    :param b: GPIO number for blue (pin B). The ``-`` pin goes to GND.
    """

    def __init__(self, r, g, b):
        self.pins = (Pin(r, Pin.OUT, value=0), Pin(g, Pin.OUT, value=0), Pin(b, Pin.OUT, value=0))

    def set(self, color):
        """Set the colour.

        :param color: tuple (r, g, b) of 0/1 values, e.g. ``rgb_led.GREEN``.
        """
        for pin, value in zip(self.pins, color):
            pin.value(value)

    def off(self):
        """Turn the LED off."""
        self.set(OFF)

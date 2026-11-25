"""Driver class for a relay module (1 Relay Module, SRD-05VDC-SL-C)."""

from machine import Pin


class Relay:
    """Single-channel relay module controlled by the IN pin.

    Some modules switch on HIGH, others on LOW (modules with an optocoupler
    usually on LOW). Check the correct ``active_low`` value with a test.

    :param pin: GPIO number connected to IN.
    :param active_low: ``True`` if the relay switches on when IN is LOW.
    """

    def __init__(self, pin, active_low=True):
        self.active_low = active_low
        self.pin = Pin(pin, Pin.OUT)
        #: ``True`` while the relay is switched on.
        self.is_on = False
        self.off()

    def on(self):
        """Switch the relay on."""
        self.pin.value(0 if self.active_low else 1)
        self.is_on = True

    def off(self):
        """Switch the relay off."""
        self.pin.value(1 if self.active_low else 0)
        self.is_on = False

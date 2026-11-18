"""Třída pro relé modul (1 Relay Module, SRD-05VDC-SL-C)."""

from machine import Pin


class Relay:
    """Jednokanálový relé modul ovládaný pinem IN.

    Některé moduly spínají při HIGH, jiné při LOW (s optočlenem většinou LOW).
    Správné nastavení ``active_low`` je potřeba ověřit testem.

    :param pin: číslo GPIO připojené na IN.
    :param active_low: ``True`` když relé sepne při LOW na IN.
    """

    def __init__(self, pin, active_low=True):
        self.active_low = active_low
        self.pin = Pin(pin, Pin.OUT)
        self.off()

    def on(self):
        """Sepne relé."""
        self.pin.value(0 if self.active_low else 1)
        #: ``True`` když je relé sepnuté.
        self.is_on = True

    def off(self):
        """Rozepne relé."""
        self.pin.value(1 if self.active_low else 0)
        self.is_on = False

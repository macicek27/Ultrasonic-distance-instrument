"""Simple driver class for a 4-digit 7-segment display with the TM1637 chip."""

from machine import Pin
from time import sleep_us

# segment patterns for digits 0-9 (bit 0 = segment a ... bit 6 = segment g)
_DIGITS = (0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F)
_MINUS = 0x40
_BLANK = 0x00
_E = 0x79
_R = 0x50
_DP = 0x80   # decimal point (bit 7 of a digit)


class TM1637:
    """4-digit display with the TM1637 controller (CLK and DIO pins).

    The controller uses a two-wire protocol similar to I2C, but without an
    address. Power the module from 3.3 V, not 5 V: its pull-up resistors
    would otherwise put 5 V on the Pico pins.

    :param clk: GPIO number connected to CLK.
    :param dio: GPIO number connected to DIO.
    :param brightness: brightness 0-7.
    """

    def __init__(self, clk, dio, brightness=4):
        self.clk = Pin(clk, Pin.OUT, value=1)
        self.dio = Pin(dio, Pin.OUT, value=1)
        self.brightness = brightness
        self.clear()

    # --- public methods -------------------------------------------------------
    def show_segments(self, segs):
        """Show 4 raw segment bytes (custom characters).

        :param segs: list of 4 numbers, each one sets the segments of one digit.
        """
        self._command(0x40)                 # data write, auto-increment address
        self._start()
        self._write_byte(0xC0)              # address of the first digit
        for s in segs:
            self._write_byte(s)
        self._stop()
        self._command(0x88 | (self.brightness & 0x07))  # display on + brightness

    def show_number(self, number):
        """Show an integer 0-9999, right-aligned.

        :param number: integer; values outside 0-9999 are shown as ``----``.
        """
        if number < 0 or number > 9999:
            self.show_dashes()
            return
        segs = [_BLANK, _BLANK, _BLANK, _BLANK]
        for i in range(3, -1, -1):
            segs[i] = _DIGITS[number % 10]
            number //= 10
            if number == 0:
                break
        self.show_segments(segs)

    def show_decimal(self, value, decimals=1, colon=False):
        """Show a number with decimal places, e.g. ``29.6``.

        :param value: number to show (0 or more).
        :param decimals: number of decimal places (0-3), used when ``colon`` is False.
        :param colon: ``True`` for "clock" modules that have only a colon between
            digits 2 and 3 instead of decimal points. The colon is then used as
            the decimal separator: values below 100 are shown with one decimal
            place (``45:6``), larger values as a whole number (``123``).
        :returns: nothing; values that do not fit into 4 digits are shown as ``----``.
        """
        if colon:
            self._show_with_colon(value)
            return
        n = round(value * 10 ** decimals)
        if value < 0 or n > 9999:
            self.show_dashes()
            return
        segs = [_BLANK, _BLANK, _BLANK, _BLANK]
        for i in range(3, -1, -1):
            segs[i] = _DIGITS[n % 10]
            n //= 10
            # stop at the first leading zero, but keep the digit before the point
            if n == 0 and i <= 3 - decimals:
                break
        if decimals > 0:
            segs[3 - decimals] |= _DP
        self.show_segments(segs)

    def show_dashes(self):
        """Show ``----`` (e.g. nothing in range)."""
        self.show_segments([_MINUS] * 4)

    def show_error(self):
        """Show ``Err`` (sensor error)."""
        self.show_segments([_E, _R, _R, _BLANK])

    def clear(self):
        """Turn all segments off."""
        self.show_segments([_BLANK] * 4)

    def _show_with_colon(self, value):
        # the colon is bit 7 of the second digit, so the layout is "DD:D "
        n = round(value * 10)               # tenths
        if value < 0:
            self.show_dashes()
        elif n >= 1000:                     # 100 cm and more -> whole number
            self.show_number(round(value))
        else:
            tens = n // 100
            ones = (n // 10) % 10
            tenths = n % 10
            first = _DIGITS[tens] if tens else _BLANK
            self.show_segments([first, _DIGITS[ones] | _DP, _DIGITS[tenths], _BLANK])

    # --- low-level protocol ---------------------------------------------------
    def _start(self):
        self.dio.value(0)
        sleep_us(5)
        self.clk.value(0)
        sleep_us(5)

    def _stop(self):
        self.dio.value(0)
        sleep_us(5)
        self.clk.value(1)
        sleep_us(5)
        self.dio.value(1)
        sleep_us(5)

    def _write_byte(self, data):
        for _ in range(8):                  # least significant bit first
            self.dio.value(data & 1)
            data >>= 1
            sleep_us(5)
            self.clk.value(1)
            sleep_us(5)
            self.clk.value(0)
        # 9th clock = acknowledge (ACK) from the chip, its value is not read
        self.dio.value(0)
        sleep_us(5)
        self.clk.value(1)
        sleep_us(5)
        self.clk.value(0)

    def _command(self, cmd):
        self._start()
        self._write_byte(cmd)
        self._stop()

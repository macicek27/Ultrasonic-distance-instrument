"""Jednoduchá třída pro 4místný 7segmentový displej s řadičem TM1637."""

from machine import Pin
from time import sleep_us

# segmenty pro číslice 0-9 (bit 0 = segment a ... bit 6 = segment g)
_DIGITS = (0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F)
_MINUS = 0x40
_BLANK = 0x00
_E = 0x79
_R = 0x50


class TM1637:
    """Displej se 4 číslicemi a řadičem TM1637 (piny CLK a DIO).

    Řadič komunikuje dvěma vodiči podobně jako I2C, ale bez adresy.
    Modul napájejte z 3,3 V, ne z 5 V: pull-up rezistory na modulu by
    jinak přivedly 5 V na piny Pica.

    :param clk: číslo GPIO připojené na CLK.
    :param dio: číslo GPIO připojené na DIO.
    :param brightness: jas 0-7.
    """

    def __init__(self, clk, dio, brightness=4):
        self.clk = Pin(clk, Pin.OUT, value=1)
        self.dio = Pin(dio, Pin.OUT, value=1)
        self.brightness = brightness
        self.clear()

    # --- veřejné metody -------------------------------------------------------
    def show_segments(self, segs):
        """Zobrazí 4 bajty segmentů (vlastní znaky).

        :param segs: seznam 4 čísel, každé určuje rozsvícené segmenty jedné číslice.
        """
        self._command(0x40)                 # zápis dat, automatický posun adresy
        self._start()
        self._write_byte(0xC0)              # adresa první číslice
        for s in segs:
            self._write_byte(s)
        self._stop()
        self._command(0x88 | (self.brightness & 0x07))  # displej zapnout + jas

    def show_number(self, number):
        """Zobrazí celé číslo 0-9999 zarovnané doprava.

        :param number: celé číslo; větší než 9999 se zobrazí jako ``----``.
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

    def show_dashes(self):
        """Zobrazí ``----`` (např. nic v dosahu)."""
        self.show_segments([_MINUS] * 4)

    def show_error(self):
        """Zobrazí ``Err`` (chyba senzoru)."""
        self.show_segments([_E, _R, _R, _BLANK])

    def clear(self):
        """Zhasne displej."""
        self.show_segments([_BLANK] * 4)

    # --- nízkoúrovňová komunikace ---------------------------------------------
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
        for _ in range(8):                  # posílá se od nejnižšího bitu
            self.dio.value(data & 1)
            data >>= 1
            sleep_us(5)
            self.clk.value(1)
            sleep_us(5)
            self.clk.value(0)
        # devátý takt = potvrzení (ACK) od řadiče, jeho hodnotu nečteme
        self.dio.value(0)
        sleep_us(5)
        self.clk.value(1)
        sleep_us(5)
        self.clk.value(0)

    def _command(self, cmd):
        self._start()
        self._write_byte(cmd)
        self._stop()

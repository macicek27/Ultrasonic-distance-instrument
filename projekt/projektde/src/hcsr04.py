"""Třída pro ultrazvukový senzor vzdálenosti HC-SR04."""

from machine import Pin, time_pulse_us
from time import sleep_us

STATUS_OK = "ok"
STATUS_OUT_OF_RANGE = "out_of_range"
STATUS_ERROR = "error"


class HCSR04:
    """Ultrazvukový senzor HC-SR04.

    Senzor po 10 µs pulzu na TRIG vyšle ultrazvuk a na pinu ECHO vrátí pulz,
    jehož délka odpovídá době letu zvuku k překážce a zpět.

    :param trig_pin: číslo GPIO připojené na TRIG.
    :param echo_pin: číslo GPIO připojené na ECHO (přes dělič 5 V -> 3,3 V).
    :param timeout_us: jak dlouho nejvýš čekat na pulz (30 000 µs odpovídá ~5 m).
    :param scale: kalibrace - násobek naměřené vzdálenosti (1.0 = bez korekce).
    :param offset_cm: kalibrace - posun v cm, přičte se po vynásobení.
    """

    MIN_CM = 2
    MAX_CM = 400
    #: Rychlost zvuku ve vzduchu při 20 °C (cm za µs).
    SPEED_CM_PER_US = 0.0343

    def __init__(self, trig_pin, echo_pin, timeout_us=30000, scale=1.0, offset_cm=0.0):
        self.trig = Pin(trig_pin, Pin.OUT, value=0)
        self.echo = Pin(echo_pin, Pin.IN)
        self.timeout_us = timeout_us
        self.scale = scale
        self.offset_cm = offset_cm
        #: Výsledek posledního měření: ``"ok"``, ``"out_of_range"`` nebo ``"error"``.
        self.status = STATUS_ERROR

    def distance_cm(self):
        """Změří vzdálenost.

        Funkce čeká na pulz ECHO, nejdéle zhruba ``timeout_us`` (30 ms).

        :returns: vzdálenost v cm, nebo ``None`` když měření neplatí.
            Proč neplatí, říká :attr:`status`:
            ``"error"`` = ECHO vůbec nepřišlo (zkontrolovat zapojení),
            ``"out_of_range"`` = nic v dosahu nebo mimo rozsah 2-400 cm.
        """
        # 10 µs pulz na TRIG spustí měření
        self.trig.value(1)
        sleep_us(10)
        self.trig.value(0)

        pulse_us = time_pulse_us(self.echo, 1, self.timeout_us)
        if pulse_us == -2:      # ECHO nezačalo -> senzor nereaguje
            self.status = STATUS_ERROR
            return None
        if pulse_us == -1:      # ECHO trvalo moc dlouho -> nic v dosahu
            self.status = STATUS_OUT_OF_RANGE
            return None

        cm = pulse_us * self.SPEED_CM_PER_US / 2    # zvuk letí tam a zpět
        cm = cm * self.scale + self.offset_cm       # kalibrace
        if cm < self.MIN_CM or cm > self.MAX_CM:
            self.status = STATUS_OUT_OF_RANGE
            return None
        self.status = STATUS_OK
        return cm

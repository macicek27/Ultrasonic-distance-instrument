"""Driver class for the HC-SR04 ultrasonic distance sensor."""

from machine import Pin, time_pulse_us
from time import sleep_us

STATUS_OK = "ok"
STATUS_OUT_OF_RANGE = "out_of_range"
STATUS_ERROR = "error"


class HCSR04:
    """HC-SR04 ultrasonic distance sensor.

    A 10 us pulse on TRIG starts a measurement. The sensor then sends an
    ultrasonic burst and sets ECHO high for the time the sound needs to
    travel to the obstacle and back.

    :param trig_pin: GPIO number connected to TRIG.
    :param echo_pin: GPIO number connected to ECHO (via a 5 V -> 3.3 V divider).
    :param timeout_us: maximum time to wait for the pulse (30 000 us is ~5 m).
    :param scale: calibration - multiplier of the measured distance (1.0 = none).
    :param offset_cm: calibration - offset in cm added after scaling.
    """

    MIN_CM = 2
    MAX_CM = 400
    #: Speed of sound in air at 20 degC (cm per us).
    SPEED_CM_PER_US = 0.0343

    def __init__(self, trig_pin, echo_pin, timeout_us=30000, scale=1.0, offset_cm=0.0):
        self.trig = Pin(trig_pin, Pin.OUT, value=0)
        self.echo = Pin(echo_pin, Pin.IN)
        self.timeout_us = timeout_us
        self.scale = scale
        self.offset_cm = offset_cm
        #: Result of the last measurement: ``"ok"``, ``"out_of_range"`` or ``"error"``.
        self.status = STATUS_ERROR
        #: Raw ECHO pulse width of the last measurement in us (negative = timeout).
        self.last_pulse_us = -2

    def distance_cm(self):
        """Measure the distance.

        Waits for the ECHO pulse, at most about ``timeout_us`` (30 ms).

        :returns: distance in cm, or ``None`` if the measurement is not valid.
            :attr:`status` tells why:
            ``"error"`` = no ECHO pulse at all (check wiring and power),
            ``"out_of_range"`` = nothing in range or outside 2-400 cm.
        """
        # a 10 us pulse on TRIG starts the measurement
        self.trig.value(1)
        sleep_us(10)
        self.trig.value(0)

        pulse_us = time_pulse_us(self.echo, 1, self.timeout_us)
        self.last_pulse_us = pulse_us
        if pulse_us == -2:      # ECHO never went high -> sensor does not respond
            self.status = STATUS_ERROR
            return None
        if pulse_us == -1:      # ECHO high for too long -> no obstacle in range
            self.status = STATUS_OUT_OF_RANGE
            return None

        cm = pulse_us * self.SPEED_CM_PER_US / 2    # sound travels there and back
        cm = cm * self.scale + self.offset_cm       # calibration
        if cm < self.MIN_CM or cm > self.MAX_CM:
            self.status = STATUS_OUT_OF_RANGE
            return None
        self.status = STATUS_OK
        return cm

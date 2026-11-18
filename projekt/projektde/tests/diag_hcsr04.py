"""Diagnostika HC-SR04 - vypíše surovou délku pulzu Echo.

Nepotřebuje žádné další soubory. Spusťte: pravým tlačítkem do kódu
-> MicroPico -> Run Current File on Board.

Jak číst výsledek:
  pulz 1000-3000 us  -> senzor funguje (1750 us je asi 30 cm)
  pulz kolem 38000 us -> senzor nezachytil odraz (mířit kolmo na knihu/zeď)
  Echo v klidu: 1 nebo pulz -1 -> Echo je pořád v 1 (chyba zapojení)
  pulz -2            -> Echo vůbec nepřišlo (chyba zapojení)
"""
from machine import Pin, time_pulse_us
import time

trig = Pin(14, Pin.OUT, value=0)  # GP14
echo = Pin(15, Pin.IN)            # GP15 (přes dělič)

for i in range(10):
    klid = echo.value()
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    pulz = time_pulse_us(echo, 1, 60000)
    if pulz > 0:
        print("Echo v klidu:", klid, "  pulz:", pulz, "us  =", round(pulz * 0.0343 / 2, 1), "cm")
    else:
        print("Echo v klidu:", klid, "  pulz:", pulz)
    time.sleep_ms(200)

"""Test RGB LED, relé a tlačítka.

Na Pico nahrajte config.py, rgb_led.py a relay.py, pak spusťte tento soubor.
Pokud relé cvaká obráceně (sepne při "VYP"), změňte RELAY_ACTIVE_LOW v config.py.
"""
from time import sleep_ms
from machine import Pin
import config
from rgb_led import RgbLed, GREEN, YELLOW, RED, BLUE
from relay import Relay

led = RgbLed(config.LED_R_PIN, config.LED_G_PIN, config.LED_B_PIN)
relay = Relay(config.RELAY_PIN, config.RELAY_ACTIVE_LOW)
button = Pin(config.BUTTON_PIN, Pin.IN, Pin.PULL_UP)

for name, color in (("zelena", GREEN), ("zluta", YELLOW), ("cervena", RED), ("modra", BLUE)):
    print("LED:", name)
    led.set(color)
    sleep_ms(1000)
led.off()

print("rele ZAP")
relay.on()
sleep_ms(2000)
print("rele VYP")
relay.off()

print("Mackejte tlacitko (10 s)...")
for i in range(500):
    if button.value() == 0:
        led.set(BLUE)
    else:
        led.off()
    sleep_ms(20)
led.off()
print("hotovo")

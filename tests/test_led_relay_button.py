"""Stand-alone test of the RGB LED, relay and push button.

Upload config.py, rgb_led.py and relay.py to the Pico, then run this file.
If the relay clicks the other way round (on at "relay OFF"), change
RELAY_ACTIVE_LOW in config.py.
"""
from time import sleep_ms
from machine import Pin
import config
from rgb_led import RgbLed, GREEN, PURPLE, RED, BLUE
from relay import Relay

led = RgbLed(config.LED_R_PIN, config.LED_G_PIN, config.LED_B_PIN)
relay = Relay(config.RELAY_PIN, config.RELAY_ACTIVE_LOW)
button = Pin(config.BUTTON_PIN, Pin.IN, Pin.PULL_UP)

for name, color in (("green", GREEN), ("purple", PURPLE), ("red", RED), ("blue", BLUE)):
    print("LED:", name)
    led.set(color)
    sleep_ms(1000)
led.off()

print("relay ON")
relay.on()
sleep_ms(2000)
print("relay OFF")
relay.off()

print("Press the button (10 s)...")
for i in range(500):
    if button.value() == 0:
        led.set(BLUE)
    else:
        led.off()
    sleep_ms(20)
led.off()
print("done")

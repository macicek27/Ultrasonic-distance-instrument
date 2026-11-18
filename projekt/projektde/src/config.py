"""Nastavení projektu: piny, prahy vzdálenosti a periody úloh.

Všechna čísla pinů jsou jen tady, ostatní soubory je berou z config.py.
Všechny použité GPIO jsou v sekci "Digital" na rozšiřující desce
(u každého pinu je trojice D / 3V3 / GND).
"""

# --- HC-SR04 ultrazvukový senzor (napájení 5 V z VBUS) ---------------------
TRIG_PIN = 14          # GP14
ECHO_PIN = 15          # GP15 - POZOR: přes dělič 1k/2k (ECHO má 5 V)!

# Kalibrace HC-SR04 (týden 2, měření 10 / 30 / 100 cm proti metru):
# skutečná vzdálenost = CAL_SCALE * naměřená + CAL_OFFSET_CM
CAL_SCALE = 0.972
CAL_OFFSET_CM = -5.0

# --- TM1637 4místný displej (napájení 3,3 V!) --------------------------------
TM_CLK_PIN = 16        # GP16
TM_DIO_PIN = 17        # GP17
TM_BRIGHTNESS = 4      # jas 0-7

# --- RGB LED modul (společná katoda, rezistory jsou na modulu) ---------------
LED_R_PIN = 18         # GP18
LED_G_PIN = 19         # GP19
LED_B_PIN = 20         # GP20

# --- Relé modul (napájení 5 V z VBUS) ----------------------------------------
RELAY_PIN = 21         # GP21
RELAY_ACTIVE_LOW = True  # většina těchto modulů spíná při LOW - ověřit testem!

# --- Tlačítko (proti GND, interní pull-up) -----------------------------------
BUTTON_PIN = 22        # GP22

# --- Prahy vzdálenosti (cm) --------------------------------------------------
FAR_CM = 100           # >= 100 cm       -> zelená
NEAR_CM = 30           # 30 az 100 cm    -> žlutá
                       # < 30 cm         -> červená + sepne relé

# --- Periody úloh (ms) -------------------------------------------------------
MEASURE_PERIOD_MS = 100    # měření vzdálenosti 10x za sekundu
DISPLAY_PERIOD_MS = 200    # obnova displeje 5x za sekundu
BUTTON_PERIOD_MS = 20      # čtení tlačítka (zároveň ošetření zákmitů)

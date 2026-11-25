"""Project configuration: pins, distance thresholds and task periods.

All pin numbers are defined only here; the other modules import them.
Every GPIO used is in the "Digital" section of the expansion board
(each pin has a D / 3V3 / GND triple).
"""

# --- HC-SR04 ultrasonic sensor (5 V supply from VBUS) -----------------------
TRIG_PIN = 14          # GP14
ECHO_PIN = 15          # GP15 - via 1k/2k voltage divider (ECHO is 5 V)!

# HC-SR04 calibration: real_distance = CAL_SCALE * measured + CAL_OFFSET_CM
# The ~5 cm offset from the first measurement was not confirmed by a second,
# careful measurement (error within +-3 cm without correction), so the
# correction is disabled.
CAL_SCALE = 1.0
CAL_OFFSET_CM = 0.0

# --- TM1637 4-digit display (3.3 V supply!) ---------------------------------
TM_CLK_PIN = 16        # GP16
TM_DIO_PIN = 17        # GP17
TM_BRIGHTNESS = 4      # brightness 0-7
TM_COLON = True        # our module has a colon (clock type), not decimal points

# --- RGB LED module (common cathode, resistors are on the module) -----------
LED_R_PIN = 18         # GP18
LED_G_PIN = 19         # GP19
LED_B_PIN = 20         # GP20

# --- Relay module (5 V supply from VBUS) ------------------------------------
RELAY_PIN = 21         # GP21
RELAY_ACTIVE_LOW = True  # module switches on LOW (checked by test)

# --- Push button (to GND, internal pull-up) ---------------------------------
BUTTON_PIN = 22        # GP22

# --- Distance thresholds (cm) -----------------------------------------------
FAR_CM = 50            # >= 50 cm       -> green
NEAR_CM = 30           # 30 to 50 cm    -> purple
                       # < 30 cm        -> red + relay on

# --- Task periods (ms) ------------------------------------------------------
MEASURE_PERIOD_MS = 100    # distance measurement 10x per second
DISPLAY_PERIOD_MS = 200    # display refresh 5x per second
BUTTON_PERIOD_MS = 20      # button polling (also debounces the button)

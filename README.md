# Ultrasonic-distance-instrument

## 1. O projektu
- **Popis problému:** Zařízení řeší bezkontaktní měření vzdálenosti k překážce v reálném čase. Slouží jako opticko-akustický parkovací senzor nebo indikátor vzdálenosti.
- **Klíčová funkce :** Pravidelné měření vzdálenosti v pevném intervalu, zobrazení naměřené hodnoty na displeji a vizuální/akustická signalizace blízko/daleko.

## 2. Tým a rozdělení odpovědností
- **Marcel Hrbáček** – 
- **Matěj Dostál** –
- **Matouš Dorazil** –
  
## 3. Hardware & Komponenty (Component List)
| Komponenta | Typ / Označení | Počet | Poznámka |
| :--- | :--- | :---: | :--- |
| Řídicí deska | STM32 / ESP32 / Arduino | 1 | Hlavní MCU |
| Ultrazvukový senzor | HC-SR04 | 1 | Měření vzdálenosti (Trigger / Echo)[cite: 2] |
| Displej | Sériový 4-místný 7-seg / Nokia 5110 (SPI) | 1 | Zobrazení naměřené vzdálenosti[cite: 2] |
| Napěťový dělič / Shifter | Rezistory (např. 1kΩ + 2kΩ) | 1 | Úprava 5V Echo signálu na 3.3V pro MCU logic[cite: 2] |
| Signalizace | Buzzer / LED | 1–3 | Akustický a vizuální alarm při přiblížení[cite: 2] |

## 4. Architektura a Zapojení
### Pin & Bus Plan
- **HC-SR04 Trigger:** GPIO Output (impuls 10 µs)
- **HC-SR04 Echo:** GPIO Input (s napěťovým děličem na 3.3V)[cite: 2]
- **Displej (SPI / Sériový):** SPI SCK, MOSI, CS (případně RX/TX podle typu displeje)[cite: 2]
- **Alarm / LED Indikace:** GPIO Output (PWM / digital)[cite: 2]

### Timing & Concurrency Plan
- **Periodické měření:** Měření vzdálenosti probíhá neblokujícím způsobem v pevném intervalu (např. každých 60 ms)[cite: 2].
- **Aktualizace displeje:** Obnovování zobrazení naměřené hodnoty 10× za sekundu[cite: 2].
- **Prahový alarm (Threshold Alarm):** Sledování minimální/maximální vzdálenosti (peak/minimum tracking) a okamžitá změna frekvence pípání/blikání dle vzdálenosti[cite: 2].

## 5. Blokové schéma

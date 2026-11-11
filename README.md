# Ultrasonic distance instrument

Bezkontaktní měřič vzdálenosti s ultrazvukovým senzorem HC-SR04 na **Raspberry Pi Pico W** v **MicroPythonu**.
Funguje jako opticko-akustický parkovací senzor: měří vzdálenost v pevném intervalu, zobrazuje ji na displeji
a signalizuje přiblížení LED diodami a bzučákem.

> Projekt do kurzu MicroPython (téma 6 – *Ultrasonic distance instrument*).

---

## 1. O projektu

- **Problém:** Bezkontaktní měření vzdálenosti k překážce v reálném čase a srozumitelná indikace „blízko / daleko“.
- **Klíčová funkce (minimum):** Měření vzdálenosti každých 60 ms, zobrazení hodnoty na displeji Nokia 5110
  a vizuální indikace blízko/daleko (zelená / žlutá / červená LED).
- **Rozšíření (až po splnění minima):**
  - prahový alarm s bzučákem, který pípá tím rychleji, čím je překážka blíž (parkovací senzor),
  - sledování minimální a maximální naměřené vzdálenosti (reset tlačítkem),
  - sloupcový graf vzdálenosti na displeji.

## 2. Tým a rozdělení odpovědností

| Člen | Hlavní zodpovědnost | Další |
| :--- | :--- | :--- |
| **Marcel Hrbáček** | Senzor HC-SR04: třída `HCSR04`, dělič napětí, měření přesnosti a rozsahu | Testy senzoru, měření do dokumentace |
| **Matěj Dostál** | Displej Nokia 5110: třída `PCD8544`, uživatelské rozhraní (`ui.py`) | Schéma zapojení, poster |
| **Matouš Dorazil** | Alarm (`alarm.py`), integrace v `main.py`, plán časování (`asyncio`) | Sphinx dokumentace, video |

## 3. Hardware

| Komponenta | Typ / označení | Počet | Poznámka |
| :--- | :--- | :---: | :--- |
| Řídicí deska | Raspberry Pi Pico W | 1 | MicroPython, logika 3,3 V |
| Ultrazvukový senzor | HC-SR04 | 1 | Napájení 5 V, rozsah ~2–400 cm, výstup ECHO má úroveň 5 V |
| Dělič napětí | rezistory 1 kΩ + 2 kΩ | 1 sada | ECHO 5 V → ~3,3 V pro GPIO Pica |
| Displej | Nokia 5110 (řadič PCD8544), SPI | 1 | 84 × 48 px, napájení 3,3 V |
| LED | zelená, žlutá, červená | 3 | každá s rezistorem 330 Ω |
| Bzučák | pasivní piezo bzučák | 1 | řízený PWM; magnetický bzučák jen přes tranzistor |
| Tlačítko | mikrospínač | 1 | reset min/max, interní pull-up |
| Ostatní | nepájivé pole, vodiče, USB kabel | – | |

## 4. Návrh

### 4.2 Zapojení (pin/bus plán)










# ⚖️ DACH Scheinselbstständigkeit- & Statusfeststellungs-Prüfer 2026 (§ 7a SGB IV, ASVG, AHVG)

[![CI](https://github.com/DACHDigitalwerk/statusfeststellung-scheinselbststaendigkeit-rechner-dach/actions/workflows/ci.yml/badge.svg)](https://github.com/DACHDigitalwerk/statusfeststellung-scheinselbststaendigkeit-rechner-dach/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Hochpräzise, modulare Python-Bibliothek und CLI-Tool zur automatisierten Prüfung und Risikoeinstufung von **Scheinselbstständigkeit, Clearing-Verfahren nach § 7a SGB IV der DRV Bund, österreichischer Abgrenzung (ASVG) und Schweizer Beurteilung (AHVG) 2026**.

🌐 **Interaktives Web-Tool & Kriterien-Prüfer:**  
Besuchen Sie unser kostenloses, 100 % clientseitiges Web-Tool:  
👉 **[DACH Scheinselbstständigkeit & Statusfeststellung-Prüfer 2026](https://dachdigitalwerk.github.io/statusfeststellung-scheinselbststaendigkeit-rechner/)**

---

## 🚀 Kernfunktionen

### 1. 🇩🇪 Deutschland (§ 7a SGB IV, DRV Bund & BAG/BSG Rechtsprechung)
- **Gesetzliche Kriterienkataloge:**
  - Weisungsfreiheit bei Ort, Zeit und Art der Ausführung
  - Ausschluss der Eingliederung in fremde Betriebsabläufe
  - Unternehmerisches Kapital- und Verlustrisiko
  - Prüfung der 5/6-Umsatzgrenze (§ 2 Satz 1 Nr. 9 SGB VI – arbeitnehmerähnliche Selbstständige)
  - Privilegierung bei Beschäftigung eigener versicherungspflichtiger Mitarbeiter
- **Finanzielle Risikosimulation für Auftraggeber:**
  - Berechnung der 4-jährigen Nachzahlungsverpflichtung für Gesamtsozialversicherungsbeiträge (~40 % auf Nettohonorare gem. § 25 SGB IV)
  - Berechnung gesetzlicher Säumniszuschläge (1 % pro Monat gem. § 24 SGB IV = 12 % p.a.)

### 2. 🇦🇹 Österreich (ASVG / ABGB)
- Abgrenzung von echtem Dienstvertrag (§ 4 Abs. 2 ASVG), freiem Dienstvertrag (§ 4 Abs. 4 ASVG) und Werkvertrag (§ 1151 ABGB).

### 3. 🇨🇭 Schweiz (AHVG)
- Kriterienkatalog der kantonalen Ausgleichskassen für Selbständigerwerbende vs. Unselbständigerwerbende (Art. 9 AHVG).

---

## 📦 Installation

```bash
pip install git+https://github.com/DACHDigitalwerk/statusfeststellung-scheinselbststaendigkeit-rechner-dach.git
```

---

## 💻 Verwendung

### CLI

```bash
# Prüfung mit hohem Grad an Selbstständigkeit
dach-statusfeststellung --capital-risk --own-hours --own-location --own-equipment --own-marketing --own-employees

# Prüfung mit Scheinselbstständigkeits-Risiko & Nachzahlungssimulation
dach-statusfeststellung --integrated-hierarchy --client-email --absence-approval --single-client-pct 100 --annual-fees 90000 --audit-years 3
```

JSON-Ausgabe:
```bash
dach-statusfeststellung --capital-risk --own-hours --json
```

---

## 🧪 Tests

```bash
pytest -v
```

---

## ⚖️ Rechtlicher Hinweis
Dieses Open-Source-Werkzeug dient der technischen Orientierung und Risikoabschätzung. Es stellt keine Rechts- oder Steuerberatung im Sinne des § 2 RDG bzw. § 5 StBerG dar. Für verbindliche Rechtssicherheit wird das offizielle Statusfeststellungsverfahren nach § 7a SGB IV bei der Deutschen Rentenversicherung Bund empfohlen.

---

## 📄 Lizenz
MIT License. Siehe [LICENSE](LICENSE) für Details.

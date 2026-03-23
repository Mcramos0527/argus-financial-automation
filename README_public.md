# ARGUS — Automated Reconciliation & General Unified System
### Powered by McFlow

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://github.com/Mcramos0527/argus-mcflow)

A desktop automation system that replaces a fully manual daily banking reconciliation workflow — built for a real manufacturing client managing **2 companies** and **11 bank accounts** across **6 different bank formats**.

---

## The Problem

The client's finance team spent hours every day:
- Manually copying bank transactions into 11 different Excel sheets
- Assigning accounting categories to each transaction by hand
- Building a daily bank balance summary for management
- Preparing cash register exports — all by copy/paste

Each bank (ICBC, BBVA, Mercado Pago, Bancor, Banco Nación, Galicia) exports data in a completely different format. No standardization. High error risk.

## The Solution

ARGUS reads the 3 source Excel files, normalizes all formats into a unified model, classifies every transaction, and generates 3 ready-to-use reports — in under 2 minutes, with zero manual intervention.

---

## Results

| Metric | Value |
|---|---|
| Transactions processed | 2,773 per run |
| Bank accounts covered | 11 |
| Bank formats normalized | 6 |
| Companies | 2 |
| Errors | 0 |
| Processing time | < 2 minutes |

---

## Features

- **Multi-format normalization** — handles 6 completely different bank export formats (ICBC, BBVA, Mercado Pago, Bancor, Banco Nación, Galicia)
- **Auto-detection** — identifies bank sheets automatically, no manual selection
- **Category classification** — maps 40 accounting categories, classifies each transaction as COBRO / PAGO / INTERNO
- **Daily bank summary** — generates management-ready balance report
- **Cash register export** — produces entries ready to paste into the monthly cash workbook
- **Desktop UI** — clean tkinter interface, no terminal required
- **Packaged as .exe** — delivered as a Windows executable, no Python installation needed for end users

---

## Architecture

```
argus/
├── main.py                     # Entry point
├── app/
│   ├── config.py               # Bank account & format configuration
│   ├── models.py               # Data models (Transaction, BankSummary, CajaEntry)
│   └── services/
│       ├── loader.py           # Excel file reader
│       ├── normalizer.py       # 6-format bank normalizer
│       ├── summary.py          # Daily summary generator
│       ├── exporter.py         # Excel report exporter
│       └── processor.py        # Pipeline orchestrator
│   └── ui/
│       └── main_window.py      # Desktop UI (tkinter)
```

**Core pipeline:**
```
Excel files → Loader → Normalizer → Classifier → Summary → Exporter → Excel reports
```

---

## Bank Format Support

| Bank | Format type | Debit/Credit structure |
|---|---|---|
| ICBC | Custom | Separate debit / credit columns |
| BBVA | Standard | Separate debit / credit columns |
| Mercado Pago | Digital wallet | Single signed value column |
| Bancor | Custom | Single signed value column |
| Banco Nación | Government bank | Single signed value column |
| Galicia | Standard | Separate debit / credit columns |

---

## Output Files

| File | Contents |
|---|---|
| `argus_movimientos_normalizados_[datetime].xlsx` | All transactions normalized, classified, categorized |
| `argus_resumen_bancario_[datetime].xlsx` | Daily balance summary per account and company |
| `argus_export_caja_[datetime].xlsx` | Cash register entries ready to use |

---

## Tech Stack

- **Python 3.11**
- **pandas** — data processing
- **openpyxl** — Excel read/write with full formatting
- **tkinter** — desktop UI
- **PyInstaller** — packaging as Windows .exe

---

## Running Locally

```bash
git clone https://github.com/Mcramos0527/argus-mcflow.git
cd argus-mcflow
pip install -r requirements.txt
python main.py
```

## Building the .exe

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name ARGUS main.py
```

---

## Roadmap

- **Wave 1** ✅ Normalization + Daily summary + Cash export
- **Wave 2** 🔜 ERP reconciliation engine + difference alerts
- **Wave 3** 🔜 SQLite database + REST API + web dashboard

---

## About

Built by **McFlow** — automation solutions for financial operations.

> *"Processing finances. Freeing time."*

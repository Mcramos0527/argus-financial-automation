# ARGUS — Automated Reconciliation & General Unified System
### Powered by McFlow · Wave 1

Sistema de automatización del proceso de control bancario diario para **Dario A. Delfabro S.R.L.** y **Delfabro y Cia S.R.L.**

---

## Qué hace

Automatiza el proceso manual que actualmente realiza Emiliano todos los días:

1. **Lee** los 3 archivos Excel del cliente (Movimientos, Saldos, Caja)
2. **Detecta** automáticamente las 11 cuentas bancarias (6 formatos distintos)
3. **Normaliza** todos los movimientos a un modelo unificado
4. **Clasifica** las transacciones usando las 40 categorías contables
5. **Genera** 3 archivos Excel de salida:
   - `argus_movimientos_normalizados_[fecha].xlsx`
   - `argus_resumen_bancario_[fecha].xlsx` (replica BANCOS DEL DIA)
   - `argus_export_caja_[fecha].xlsx`

## Cuentas soportadas

| Empresa | Pestaña | Banco |
|---|---|---|
| DD SRL | ICBC dd srl | ICBC |
| DD SRL | MP fondo azul | Mercado Pago Gerencia |
| DD SRL | MP fondo blanco | Mercado Pago Ventas |
| DD SRL | BBVA dd srl 486 | BBVA 486 |
| DD SRL | BBVA dd srl 487 | BBVA 487 |
| DD SRL | Bancor dd srl | Bancor |
| D y CIA | Nacion Y CIA | Banco Nación |
| D y CIA | ICBC y cia | ICBC |
| D y CIA | BBVA y cia 407 | BBVA 407 |
| D y CIA | BBVA y cia 151 | BBVA 151 |
| D y CIA | GALICIA y cia | Galicia Más |

---

## Instalación para desarrollo

```bash
# Python 3.10+
pip install -r requirements.txt
python main.py
```

## Compilar el .exe para el cliente

```bash
# En Windows, doble clic en:
build.bat

# O manualmente:
pip install pyinstaller
pyinstaller --onefile --windowed --name ARGUS --icon icon.ico main.py
```

El ejecutable queda en `dist/ARGUS.exe`.

Para generar el instalador profesional, instalar [Inno Setup](https://jrsoftware.org/isinfo.php) y compilar `installer.iss`.

---

## Estructura del proyecto

```
argus/
├── main.py                     # Punto de entrada
├── requirements.txt
├── build.bat                   # Script de compilación Windows
├── installer.iss               # Script Inno Setup (instalador)
├── app/
│   ├── config.py               # Configuración de todas las cuentas
│   ├── models.py               # Modelos de datos
│   ├── services/
│   │   ├── loader.py           # Carga de archivos Excel
│   │   ├── normalizer.py       # Normalización de 6 formatos bancarios
│   │   ├── summary.py          # Generación de resúmenes
│   │   ├── exporter.py         # Exportación a Excel
│   │   └── processor.py        # Orquestador del pipeline
│   └── ui/
│       └── main_window.py      # Interfaz gráfica
├── outputs/                    # Archivos generados
└── logs/                       # Logs del sistema
```

---

## Roadmap

- **Wave 1** ✅ MVP — Normalización + Resumen + Export
- **Wave 2** 🔜 Conciliación vs ERP Coliseo + Alertas
- **Wave 3** 🔜 Base de datos + Multi-empresa + API

---

*McFlow © 2026*

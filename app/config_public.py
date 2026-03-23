# app/config.py
# ARGUS — Automated Reconciliation & General Unified System
# Powered by McFlow
#
# Configuration file — public demo version.
# All company names, account numbers, and personal data have been replaced
# with generic placeholders.

from typing import Dict, Any

APP_NAME = "ARGUS"
APP_SUBTITLE = "Powered by McFlow"
APP_VERSION = "1.0.0"
WINDOW_SIZE = "960x680"

# ── Bank sheet mapping ───────────────────────────────────────────────────────
# Each entry defines:
#   company   : company that owns the account
#   bank      : bank name
#   header_row: row number (1-based) where headers are located
#   data_row  : first row with actual data (1-based)
#   format    : key that selects the normalizer
#   columns   : mapping original_col → normalized_field

SHEET_CONFIG: Dict[str, Dict[str, Any]] = {

    # ── Company A accounts ────────────────────────────────────────────────────
    "ICBC company_a": {
        "company": "Company A S.R.L.",
        "bank": "ICBC",
        "header_row": 5,
        "data_row": 6,
        "format": "ICBC",
        "columns": {
            "Fecha contable":            "fecha",
            "Cod de Concepto":           "cod_concepto",
            "Concepto":                  "descripcion",
            "Debito en $":               "debito",
            "Credito en $":              "credito",
            "Saldo en $":                "saldo",
            "Informacion Complementaria":"detalle",
            "Nro de cheque":             "nro_cheque",
            "Canal":                     "canal",
            "tipo concepto":             "tipo_concepto",
            "CONCEPTO2":                 "categoria_codigo",
        },
    },

    "MP account_blue": {
        "company": "Company A S.R.L.",
        "bank": "Mercado Pago Account 1",
        "header_row": 5,
        "data_row": 6,
        "format": "MP",
        "columns": {
            "Fecha":       "fecha",
            "Descripción": "descripcion",
            "ID de la":    "nro_referencia",
            "Valor":       "importe_neto",
            "Saldo":       "saldo",
            "CATEGORÍA":   "categoria_codigo",
        },
    },

    "MP account_white": {
        "company": "Company A S.R.L.",
        "bank": "Mercado Pago Account 2",
        "header_row": 5,
        "data_row": 6,
        "format": "MP",
        "columns": {
            "Fecha":       "fecha",
            "Descripción": "descripcion",
            "ID de la":    "nro_referencia",
            "Valor":       "importe_neto",
            "Saldo":       "saldo",
            "CATEGORÍA":   "categoria_codigo",
        },
    },

    "BBVA company_a 001": {
        "company": "Company A S.R.L.",
        "bank": "BBVA Account 001",
        "header_row": 5,
        "data_row": 6,
        "format": "BBVA",
        "columns": {
            "Fecha":              "fecha",
            "Fecha Valor":        "fecha_valor",
            "Concepto":           "descripcion",
            "Codigo":             "cod_concepto",
            "Número Documento":   "nro_referencia",
            "Oficina":            "sucursal",
            "Crédito":            "credito",
            "Débito":             "debito",
            "Detalle":            "detalle",
            "Saldo disponible":   "saldo",
            "CATEGORÍA":          "categoria_codigo",
        },
    },

    "BBVA company_a 002": {
        "company": "Company A S.R.L.",
        "bank": "BBVA Account 002",
        "header_row": 5,
        "data_row": 6,
        "format": "BBVA",
        "columns": {
            "Fecha":              "fecha",
            "Fecha Valor":        "fecha_valor",
            "Concepto":           "descripcion",
            "Codigo":             "cod_concepto",
            "Número Documento":   "nro_referencia",
            "Oficina":            "sucursal",
            "Crédito":            "credito",
            "Débito":             "debito",
            "Detalle":            "detalle",
            "Saldo disponible":   "saldo",
            "CATEGORÍA":          "categoria_codigo",
        },
    },

    "Bancor company_a": {
        "company": "Company A S.R.L.",
        "bank": "Bancor",
        "header_row": 5,
        "data_row": 6,
        "format": "BANCOR",
        "columns": {
            "Fecha     ":                    "fecha",
            "Nro.Comprobante     ":          "nro_referencia",
            "Concepto                                          ": "descripcion",
            "Descripcion                                                                                                                     ": "detalle",
            "Monto               ":          "importe_neto",
            "Saldo Parcial       ":          "saldo",
            "CATEGORÍA":                     "categoria_codigo",
        },
    },

    # ── Company B accounts ────────────────────────────────────────────────────
    "Nacion company_b": {
        "company": "Company B S.R.L.",
        "bank": "Banco Nación",
        "header_row": 5,
        "data_row": 6,
        "format": "NACION",
        "columns": {
            "Fecha":       "fecha",
            "Comprobante": "nro_referencia",
            "Concepto":    "descripcion",
            "Importe":     "importe_neto",
            "Saldo":       "saldo",
            "CATEGORÍA":   "categoria_codigo",
        },
    },

    "ICBC company_b": {
        "company": "Company B S.R.L.",
        "bank": "ICBC",
        "header_row": 5,
        "data_row": 6,
        "format": "ICBC",
        "columns": {
            "Fecha contable":            "fecha",
            "Cod de Concepto":           "cod_concepto",
            "Concepto":                  "descripcion",
            "Debito en $":               "debito",
            "Credito en $":              "credito",
            "Saldo en $":                "saldo",
            "Informacion Complementaria":"detalle",
            "Nro de cheque":             "nro_cheque",
            "Canal":                     "canal",
            "CATEGORÍA":                 "categoria_codigo",
        },
    },

    "BBVA company_b 001": {
        "company": "Company B S.R.L.",
        "bank": "BBVA Account 001",
        "header_row": 5,
        "data_row": 6,
        "format": "BBVA",
        "columns": {
            "Fecha":              "fecha",
            "Fecha Valor":        "fecha_valor",
            "Concepto":           "descripcion",
            "Codigo":             "cod_concepto",
            "Número Documento":   "nro_referencia",
            "Oficina":            "sucursal",
            "Crédito":            "credito",
            "Débito":             "debito",
            "Detalle":            "detalle",
            "Saldo disponible":   "saldo",
            "CATEGORÍA":          "categoria_codigo",
        },
    },

    "BBVA company_b 002": {
        "company": "Company B S.R.L.",
        "bank": "BBVA Account 002",
        "header_row": 5,
        "data_row": 6,
        "format": "BBVA",
        "columns": {
            "Fecha":              "fecha",
            "Fecha Valor":        "fecha_valor",
            "Concepto":           "descripcion",
            "Codigo":             "cod_concepto",
            "Número Documento":   "nro_referencia",
            "Oficina":            "sucursal",
            "Crédito":            "credito",
            "Débito":             "debito",
            "Detalle":            "detalle",
            "Saldo disponible":   "saldo",
            "CATEGORÍA":          "categoria_codigo",
        },
    },

    "Galicia company_b": {
        "company": "Company B S.R.L.",
        "bank": "Galicia",
        "header_row": 5,
        "data_row": 6,
        "format": "GALICIA",
        "columns": {
            "Fecha":                "fecha",
            "Tipo operación":       "tipo_concepto",
            "Comprobante":          "nro_referencia",
            "Descripción":          "descripcion",
            "Débito":               "debito",
            "Crédito":              "credito",
            "Descripción Completa": "detalle",
            "CATEGORÍA":            "categoria_codigo",
        },
    },
}

# Auxiliary sheets that are NOT bank sheets (ignored during parsing)
NON_BANK_SHEETS = {"CONCILICIACION", "CONCILIACION", "CATEGORIAS CONTABLES", "Explicacion"}

# Normalized unified model fields
NORMALIZED_FIELDS = [
    "pestaña",
    "empresa",
    "banco",
    "fecha",
    "fecha_valor",
    "descripcion",
    "detalle",
    "debito",
    "credito",
    "importe_neto",
    "saldo",
    "nro_referencia",
    "nro_cheque",
    "cod_concepto",
    "tipo_concepto",
    "canal",
    "sucursal",
    "categoria_codigo",
    "categoria_nombre",
    "tipo_movimiento",   # COBRO / PAGO / INTERNO
]

# Income categories (used to classify movement type)
INCOME_CATEGORIES = {25, 26, 27, 28, 29}

# Company colors for the UI
COMPANY_COLORS = {
    "Company A S.R.L.": "#3B8BD4",   # blue
    "Company B S.R.L.": "#E8A020",   # yellow
}

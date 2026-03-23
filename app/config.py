# app/config.py
# ARGUS — Automated Reconciliation & General Unified System
# Powered by McFlow
#
# Configuración basada en los archivos REALES del cliente Delfabro.

from typing import Dict, Any

APP_NAME = "ARGUS"
APP_SUBTITLE = "Powered by McFlow"
APP_VERSION = "1.0.0"
WINDOW_SIZE = "960x680"

# ── Mapeo de pestañas bancarias ──────────────────────────────────────────────
# Cada entrada define:
#   company   : empresa propietaria de la cuenta
#   bank      : nombre del banco
#   header_row: número de fila (1-based) donde están los encabezados
#   data_row  : primera fila con datos reales (1-based)
#   format    : clave que selecciona el normalizador
#   columns   : mapeo col_original → campo_normalizado

SHEET_CONFIG: Dict[str, Dict[str, Any]] = {

    # ── DD SRL (azul) ─────────────────────────────────────────────────────────
    "ICBC dd srl": {
        "company": "Dario A. Delfabro S.R.L.",
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
            "CONCEPTO2":                 "categoria_codigo",   # columna K = código manual
        },
    },

    "MP fondo azul": {
        "company": "Dario A. Delfabro S.R.L.",
        "bank": "Mercado Pago Gerencia (Fondo Azul)",
        "header_row": 5,
        "data_row": 6,
        "format": "MP",
        "columns": {
            "Fecha":       "fecha",
            "Descripción": "descripcion",
            "ID de la":    "nro_referencia",
            "Valor":       "importe_neto",   # positivo=crédito, negativo=débito
            "Saldo":       "saldo",
            "CATEGORÍA":   "categoria_codigo",
        },
    },

    "MP fondo blanco": {
        "company": "Dario A. Delfabro S.R.L.",
        "bank": "Mercado Pago Ventas (Fondo Blanco)",
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

    "BBVA dd srl 486": {
        "company": "Dario A. Delfabro S.R.L.",
        "bank": "BBVA 486",
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

    "BBVA dd srl 487": {
        "company": "Dario A. Delfabro S.R.L.",
        "bank": "BBVA 487",
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

    "Bancor dd srl": {
        "company": "Dario A. Delfabro S.R.L.",
        "bank": "Bancor",
        "header_row": 5,
        "data_row": 6,
        "format": "BANCOR",
        "columns": {
            "Fecha     ":                    "fecha",        # Bancor tiene espacios en los headers
            "Nro.Comprobante     ":          "nro_referencia",
            "Concepto                                          ": "descripcion",
            "Descripcion                                                                                                                     ": "detalle",
            "Monto               ":          "importe_neto",
            "Saldo Parcial       ":          "saldo",
            "CATEGORÍA":                     "categoria_codigo",
        },
    },

    # ── D y CIA (amarillo) ────────────────────────────────────────────────────
    "Nacion Y CIA": {
        "company": "Delfabro y Cia S.R.L.",
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

    "ICBC y cia": {
        "company": "Delfabro y Cia S.R.L.",
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

    "BBVA y cia 407": {
        "company": "Delfabro y Cia S.R.L.",
        "bank": "BBVA 407",
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

    "BBVA y cia 151": {
        "company": "Delfabro y Cia S.R.L.",
        "bank": "BBVA 151",
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

    "GALICIA y cia": {
        "company": "Delfabro y Cia S.R.L.",
        "bank": "Galicia Más",
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

# Pestañas auxiliares que NO son bancarias (se ignoran en el parse)
NON_BANK_SHEETS = {"CONCILICIACION", "CONCILIACION", "CATEGORIAS CONTABLES", "Explicacion"}

# Campos del modelo normalizado unificado
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

# Tipos de movimiento por categoría (25-29 son ingresos)
INCOME_CATEGORIES = {25, 26, 27, 28, 29}

# Colores de empresa para la UI
COMPANY_COLORS = {
    "Dario A. Delfabro S.R.L.": "#3B8BD4",   # azul
    "Delfabro y Cia S.R.L.":    "#E8A020",   # amarillo
}

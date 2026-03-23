# app/services/normalizer.py
# Motor de normalización: convierte los 6 formatos bancarios distintos
# al modelo unificado Transaction.

import logging
import re
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple

from app.config import SHEET_CONFIG
from app.models import Transaction

logger = logging.getLogger("argus.normalizer")


def _parse_date(value) -> Optional[date]:
    """Intenta convertir cualquier formato de fecha al tipo date."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        value = value.strip()
        # Formatos más comunes en los archivos del cliente
        for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%y", "%d/%m/%y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
    return None


def _safe_float(value) -> float:
    """Convierte a float de forma segura; retorna 0.0 si no es numérico."""
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        # Limpia separadores de miles y comas decimales argentinas
        cleaned = value.strip().replace(" ", "").replace("$", "")
        cleaned = cleaned.replace(".", "").replace(",", ".")
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    return 0.0


def _safe_str(value) -> str:
    """Convierte a string limpio."""
    if value is None:
        return ""
    s = str(value).strip()
    # Elimina fórmulas Excel que quedaron sin calcular
    if s.startswith("="):
        return ""
    return s


# ── Normalizadores por formato ────────────────────────────────────────────────

def _normalize_icbc(row: tuple, headers: Dict[str, int], cfg: dict) -> Optional[Transaction]:
    """Formato ICBC: Débito y Crédito en columnas separadas."""
    fecha = _parse_date(_get(row, headers, "Fecha contable"))
    if fecha is None:
        return None

    debito  = _safe_float(_get(row, headers, "Debito en $"))
    credito = _safe_float(_get(row, headers, "Credito en $"))
    neto    = credito - debito

    t = Transaction(
        pestaña          = cfg.get("sheet_name", ""),
        empresa          = cfg["company"],
        banco            = cfg["bank"],
        fecha            = fecha,
        descripcion      = _safe_str(_get(row, headers, "Concepto")),
        detalle          = _safe_str(_get(row, headers, "Informacion Complementaria")),
        debito           = debito,
        credito          = credito,
        importe_neto     = neto,
        saldo            = _safe_float(_get(row, headers, "Saldo en $")),
        nro_cheque       = _safe_str(_get(row, headers, "Nro de cheque")),
        cod_concepto     = _safe_str(_get(row, headers, "Cod de Concepto")),
        canal            = _safe_str(_get(row, headers, "Canal")),
        tipo_concepto    = _safe_str(_get(row, headers, "tipo concepto")),
        categoria_codigo = _parse_cat_code(_get(row, headers, "tipo concepto")),
    )
    return t


def _normalize_mp(row: tuple, headers: Dict[str, int], cfg: dict) -> Optional[Transaction]:
    """Formato Mercado Pago: un solo campo Valor (positivo=crédito, negativo=débito)."""
    fecha = _parse_date(_get(row, headers, "Fecha"))
    if fecha is None:
        return None

    neto    = _safe_float(_get(row, headers, "Valor"))
    debito  = abs(neto) if neto < 0 else 0.0
    credito = neto      if neto > 0 else 0.0

    cat_raw = _get(row, headers, "CATEGORÍA")

    t = Transaction(
        pestaña          = cfg.get("sheet_name", ""),
        empresa          = cfg["company"],
        banco            = cfg["bank"],
        fecha            = fecha,
        descripcion      = _safe_str(_get(row, headers, "Descripción")),
        nro_referencia   = _safe_str(_get(row, headers, "ID de la")),
        debito           = debito,
        credito          = credito,
        importe_neto     = neto,
        saldo            = _safe_float(_get(row, headers, "Saldo")),
        categoria_codigo = _parse_cat_code(cat_raw),
    )
    return t


def _normalize_bbva(row: tuple, headers: Dict[str, int], cfg: dict) -> Optional[Transaction]:
    """Formato BBVA: Crédito y Débito separados."""
    fecha = _parse_date(_get(row, headers, "Fecha"))
    if fecha is None:
        return None

    credito = _safe_float(_get(row, headers, "Crédito"))
    debito  = _safe_float(_get(row, headers, "Débito"))
    neto    = credito - debito
    cat_raw = _get(row, headers, "CATEGORÍA")

    t = Transaction(
        pestaña          = cfg.get("sheet_name", ""),
        empresa          = cfg["company"],
        banco            = cfg["bank"],
        fecha            = fecha,
        fecha_valor      = _parse_date(_get(row, headers, "Fecha Valor")),
        descripcion      = _safe_str(_get(row, headers, "Concepto")),
        detalle          = _safe_str(_get(row, headers, "Detalle")),
        cod_concepto     = _safe_str(_get(row, headers, "Codigo")),
        nro_referencia   = _safe_str(_get(row, headers, "Número Documento")),
        sucursal         = _safe_str(_get(row, headers, "Oficina")),
        credito          = credito,
        debito           = debito,
        importe_neto     = neto,
        saldo            = _safe_float(_get(row, headers, "Saldo disponible")),
        categoria_codigo = _parse_cat_code(cat_raw),
    )
    return t


def _normalize_bancor(row: tuple, headers: Dict[str, int], cfg: dict) -> Optional[Transaction]:
    """Formato Bancor: un solo campo Monto (positivo/negativo)."""
    # Bancor tiene headers con espacios al final — se buscan por .strip()
    fecha = _parse_date(_get_stripped(row, headers, "Fecha"))
    if fecha is None:
        return None

    neto    = _safe_float(_get_stripped(row, headers, "Monto"))
    debito  = abs(neto) if neto < 0 else 0.0
    credito = neto      if neto > 0 else 0.0
    cat_raw = _get(row, headers, "CATEGORÍA")

    t = Transaction(
        pestaña          = cfg.get("sheet_name", ""),
        empresa          = cfg["company"],
        banco            = cfg["bank"],
        fecha            = fecha,
        descripcion      = _safe_str(_get_stripped(row, headers, "Concepto")),
        detalle          = _safe_str(_get_stripped(row, headers, "Descripcion")),
        nro_referencia   = _safe_str(_get_stripped(row, headers, "Nro.Comprobante")),
        debito           = debito,
        credito          = credito,
        importe_neto     = neto,
        saldo            = _safe_float(_get_stripped(row, headers, "Saldo Parcial")),
        categoria_codigo = _parse_cat_code(cat_raw),
    )
    return t


def _normalize_nacion(row: tuple, headers: Dict[str, int], cfg: dict) -> Optional[Transaction]:
    """Formato Banco Nación: un campo Importe."""
    fecha = _parse_date(_get(row, headers, "Fecha"))
    if fecha is None:
        return None

    neto    = _safe_float(_get(row, headers, "Importe"))
    debito  = abs(neto) if neto < 0 else 0.0
    credito = neto      if neto > 0 else 0.0
    cat_raw = _get(row, headers, "CATEGORÍA")

    t = Transaction(
        pestaña          = cfg.get("sheet_name", ""),
        empresa          = cfg["company"],
        banco            = cfg["bank"],
        fecha            = fecha,
        descripcion      = _safe_str(_get(row, headers, "Concepto")),
        nro_referencia   = _safe_str(_get(row, headers, "Comprobante")),
        debito           = debito,
        credito          = credito,
        importe_neto     = neto,
        saldo            = _safe_float(_get(row, headers, "Saldo")),
        categoria_codigo = _parse_cat_code(cat_raw),
    )
    return t


def _normalize_galicia(row: tuple, headers: Dict[str, int], cfg: dict) -> Optional[Transaction]:
    """Formato Galicia Más: Débito y Crédito separados."""
    fecha = _parse_date(_get(row, headers, "Fecha"))
    if fecha is None:
        return None

    debito  = _safe_float(_get(row, headers, "Débito"))
    credito = _safe_float(_get(row, headers, "Crédito"))
    neto    = credito - debito
    cat_raw = _get(row, headers, "CATEGORÍA")

    t = Transaction(
        pestaña          = cfg.get("sheet_name", ""),
        empresa          = cfg["company"],
        banco            = cfg["bank"],
        fecha            = fecha,
        descripcion      = _safe_str(_get(row, headers, "Descripción")),
        detalle          = _safe_str(_get(row, headers, "Descripción Completa")),
        tipo_concepto    = _safe_str(_get(row, headers, "Tipo operación")),
        nro_referencia   = _safe_str(_get(row, headers, "Comprobante")),
        debito           = debito,
        credito          = credito,
        importe_neto     = neto,
        categoria_codigo = _parse_cat_code(cat_raw),
    )
    return t


# ── Helpers ───────────────────────────────────────────────────────────────────

NORMALIZERS = {
    "ICBC":    _normalize_icbc,
    "MP":      _normalize_mp,
    "BBVA":    _normalize_bbva,
    "BANCOR":  _normalize_bancor,
    "NACION":  _normalize_nacion,
    "GALICIA": _normalize_galicia,
}


def _get(row: tuple, headers: Dict[str, int], key: str):
    """Obtiene el valor de una celda por nombre de columna."""
    idx = headers.get(key)
    if idx is None or idx >= len(row):
        return None
    return row[idx]


def _get_stripped(row: tuple, headers: Dict[str, int], key: str):
    """Igual que _get pero busca la clave ignorando espacios en el header."""
    for h_key, idx in headers.items():
        if str(h_key).strip() == key.strip():
            if idx < len(row):
                return row[idx]
    return None


def _parse_cat_code(value) -> Optional[int]:
    """Extrae el código de categoría numérico."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    if isinstance(value, str):
        # A veces viene como "17" o " 17 "
        stripped = value.strip()
        try:
            return int(float(stripped))
        except ValueError:
            return None
    return None


def build_headers(header_row: tuple) -> Dict[str, int]:
    """Construye un dict {nombre_columna: índice} desde la fila de encabezados."""
    headers = {}
    for idx, cell in enumerate(header_row):
        if cell is not None:
            headers[str(cell)] = idx
    return headers


# ── Normalizador principal ────────────────────────────────────────────────────

class Normalizer:
    """Convierte filas crudas de cada pestaña bancaria al modelo Transaction."""

    def normalize_sheet(
        self,
        sheet_name: str,
        rows: List[tuple],
        categories: Dict[int, str],
    ) -> Tuple[List[Transaction], List[str]]:
        """
        Normaliza todas las filas de una pestaña.
        Retorna (transacciones, lista_de_warnings).
        """
        cfg = SHEET_CONFIG.get(sheet_name)
        if cfg is None:
            return [], [f"Pestaña '{sheet_name}' sin configuración"]

        fmt = cfg["format"]
        normalizer_fn = NORMALIZERS.get(fmt)
        if normalizer_fn is None:
            return [], [f"Formato '{fmt}' no implementado para '{sheet_name}'"]

        header_row_idx = cfg["header_row"] - 1   # 0-based
        data_row_start = cfg["data_row"] - 1      # 0-based

        if len(rows) <= header_row_idx:
            return [], [f"'{sheet_name}': no se encontró la fila de encabezados"]

        headers = build_headers(rows[header_row_idx])
        if not headers:
            return [], [f"'{sheet_name}': encabezados vacíos"]

        cfg_with_name = {**cfg, "sheet_name": sheet_name}
        transactions: List[Transaction] = []
        warnings: List[str] = []
        skipped = 0

        for row_idx, row in enumerate(rows[data_row_start:], start=data_row_start + 1):
            # Saltar filas completamente vacías
            if all(v is None or str(v).strip() == "" for v in row):
                continue

            try:
                tx = normalizer_fn(row, headers, cfg_with_name)
                if tx is None:
                    skipped += 1
                    continue

                # Enriquecer con nombre de categoría
                if tx.categoria_codigo and tx.categoria_codigo in categories:
                    tx.categoria_nombre = categories[tx.categoria_codigo]

                # Clasificar tipo de movimiento
                tx.tipo_movimiento = _classify_movement(tx)

                transactions.append(tx)

            except Exception as e:
                warnings.append(f"'{sheet_name}' fila {row_idx}: {e}")

        logger.info(
            f"'{sheet_name}' ({fmt}): {len(transactions)} transacciones, "
            f"{skipped} sin fecha, {len(warnings)} warnings"
        )
        return transactions, warnings


def _classify_movement(tx: Transaction) -> str:
    """Clasifica la transacción como COBRO, PAGO, INTERNO o SIN CLASIFICAR."""
    from app.config import INCOME_CATEGORIES

    if tx.categoria_codigo in INCOME_CATEGORIES:
        return "COBRO"

    # Por código de categoría
    if tx.categoria_codigo == 39:
        return "INTERNO"   # TRANSFER INTERNA

    # Por importe neto
    if tx.importe_neto > 0:
        return "COBRO"
    if tx.importe_neto < 0:
        return "PAGO"

    # Por columnas separadas
    if tx.credito > 0 and tx.debito == 0:
        return "COBRO"
    if tx.debito > 0 and tx.credito == 0:
        return "PAGO"

    return "SIN CLASIFICAR"

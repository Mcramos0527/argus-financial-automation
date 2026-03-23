# app/services/processor.py
# Orquesta el pipeline completo: carga → normaliza → resume → exporta.

import logging
from pathlib import Path
from typing import Callable, Optional

from app.models import ProcessResult
from app.services.loader     import ExcelLoader
from app.services.normalizer  import Normalizer
from app.services.summary    import SummaryGenerator
from app.services.exporter   import Exporter

logger = logging.getLogger("argus.processor")


class Processor:
    """Pipeline principal de ARGUS."""

    def __init__(self):
        self.loader    = ExcelLoader()
        self.normalizer = Normalizer()
        self.summarizer = SummaryGenerator()
        self.exporter  = Exporter()

    def run(
        self,
        path_movimientos: str,
        path_saldos: str,
        path_caja: str,
        output_folder: str,
        on_progress: Optional[Callable[[str], None]] = None,
    ) -> ProcessResult:
        """
        Ejecuta el pipeline completo y retorna el resultado.
        on_progress: callback para mostrar mensajes en la UI.
        """
        result = ProcessResult()

        def progress(msg: str):
            logger.info(msg)
            if on_progress:
                on_progress(msg)

        # ── 1. Cargar archivos ────────────────────────────────────────────────
        progress("Cargando Movimientos Bancarios...")
        ok, msg = self.loader.load_movimientos(path_movimientos)
        if not ok:
            result.errors.append(f"Movimientos: {msg}")
            return result

        progress("Cargando Saldos del Día...")
        ok, msg = self.loader.load_saldos(path_saldos)
        if not ok:
            result.warnings.append(f"Saldos (no crítico): {msg}")

        progress("Cargando Caja Fábrica Digital...")
        ok, msg = self.loader.load_caja(path_caja)
        if not ok:
            result.warnings.append(f"Caja (no crítico): {msg}")

        # ── 2. Categorías ─────────────────────────────────────────────────────
        progress("Leyendo tabla de categorías contables...")
        categories = self.loader.get_categories()
        if not categories:
            result.warnings.append("No se encontró la tabla de categorías.")

        # ── 3. Detectar pestañas bancarias ────────────────────────────────────
        bank_sheets = self.loader.get_bank_sheets()
        if not bank_sheets:
            result.errors.append("No se detectaron pestañas bancarias conocidas.")
            return result
        progress(f"Pestañas detectadas: {', '.join(bank_sheets)}")

        # ── 4. Normalizar cada pestaña ────────────────────────────────────────
        all_transactions = []
        for sheet_name in bank_sheets:
            progress(f"Procesando: {sheet_name}...")
            rows = self.loader.get_sheet_rows(sheet_name)
            if not rows:
                result.warnings.append(f"'{sheet_name}': sin datos")
                continue

            txs, warns = self.normalizer.normalize_sheet(sheet_name, rows, categories)
            all_transactions.extend(txs)
            result.warnings.extend(warns)
            result.sheets_processed += 1
            progress(f"  → {len(txs)} transacciones")

        result.transactions = all_transactions
        result.transactions_total = len(all_transactions)

        if result.transactions_total == 0:
            result.errors.append("No se extrajeron transacciones. Verificar formato de archivos.")
            return result

        progress(f"Total transacciones normalizadas: {result.transactions_total}")

        # ── 5. Generar resúmenes bancarios ────────────────────────────────────
        progress("Generando resumen bancario diario...")
        result.summaries = self.summarizer.generate_bank_summaries(all_transactions)
        progress(f"  → {len(result.summaries)} cuentas resumidas")

        # ── 6. Generar entradas de caja ───────────────────────────────────────
        progress("Generando export para Caja Fábrica Digital...")
        result.caja_entries = self.summarizer.generate_caja_entries(all_transactions)
        progress(f"  → {len(result.caja_entries)} entradas de caja")

        # ── 7. Exportar Excel ────────────────────────────────────────────────
        progress("Generando archivos Excel de salida...")
        generated_files = self.exporter.export_all(
            transactions  = result.transactions,
            summaries     = result.summaries,
            caja_entries  = result.caja_entries,
            output_folder = output_folder,
        )
        progress(f"Archivos generados: {len(generated_files)}")
        for f in generated_files:
            progress(f"  ✓ {Path(f).name}")

        progress("─" * 50)
        progress(f"✅ Proceso completado — {result.transactions_total} transacciones procesadas")

        return result

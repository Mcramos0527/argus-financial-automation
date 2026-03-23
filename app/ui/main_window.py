# app/ui/main_window.py
# Interfaz de usuario ARGUS — diseño limpio y profesional con tkinter nativo.

import logging
import os
import subprocess
import sys
import threading
from pathlib import Path
from tkinter import (
    BooleanVar, END, FLAT, Frame, Label, StringVar, Text,
    Tk, filedialog, messagebox, ttk
)
import tkinter as tk

from app.config import APP_NAME, APP_SUBTITLE, APP_VERSION, WINDOW_SIZE
from app.services.processor import Processor

logger = logging.getLogger("argus.ui")

# ── Paleta de colores ─────────────────────────────────────────────────────────
C_BG        = "#1E2330"   # fondo principal oscuro
C_PANEL     = "#252C3D"   # fondo paneles
C_CARD      = "#2D3548"   # fondo tarjetas
C_ACCENT    = "#4A9EFF"   # azul acento
C_SUCCESS   = "#4CAF50"   # verde éxito
C_WARNING   = "#FF9800"   # naranja advertencia
C_ERROR     = "#F44336"   # rojo error
C_TEXT      = "#E8EAF0"   # texto principal
C_TEXT_MUTED= "#8B92A5"   # texto secundario
C_BORDER    = "#3A4255"   # bordes
C_BTN_HOVER = "#357ADB"   # hover botones
C_DD_SRL    = "#3B8BD4"   # azul DD SRL
C_D_CIA     = "#E8A020"   # amarillo D y CIA


class ArgusApp:
    """Ventana principal de ARGUS."""

    def __init__(self):
        self.root = Tk()
        self.processor = Processor()
        self._setup_window()
        self._build_ui()
        self._processing = False

    # ── Setup ventana ─────────────────────────────────────────────────────────

    def _setup_window(self):
        self.root.title(f"{APP_NAME} — {APP_SUBTITLE}")
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(880, 620)
        self.root.configure(bg=C_BG)
        self.root.resizable(True, True)

        # Intentar ícono (si existe)
        try:
            icon_path = Path(__file__).parent.parent.parent / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception:
            pass

        # Variables de archivo
        self.path_movimientos = StringVar()
        self.path_saldos      = StringVar()
        self.path_caja        = StringVar()
        self.path_output      = StringVar(value=str(Path.home() / "ARGUS_Outputs"))

    # ── Construcción de UI ────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Header ────────────────────────────────────────────────────────────
        header = Frame(self.root, bg="#141824", height=64)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        logo_frame = Frame(header, bg="#141824")
        logo_frame.pack(side="left", padx=24, pady=12)

        Label(
            logo_frame, text="ARGUS", bg="#141824",
            fg=C_ACCENT, font=("Segoe UI", 22, "bold")
        ).pack(side="left")
        Label(
            logo_frame, text=f"  {APP_SUBTITLE}  v{APP_VERSION}", bg="#141824",
            fg=C_TEXT_MUTED, font=("Segoe UI", 10)
        ).pack(side="left", pady=4)

        Label(
            header,
            text="Sistema de Conciliación Bancaria Automatizada",
            bg="#141824", fg=C_TEXT_MUTED,
            font=("Segoe UI", 9)
        ).pack(side="right", padx=24)

        # ── Contenedor principal (2 columnas) ─────────────────────────────────
        main = Frame(self.root, bg=C_BG)
        main.pack(fill="both", expand=True, padx=16, pady=12)

        # Columna izquierda — archivos + configuración
        left = Frame(main, bg=C_BG, width=420)
        left.pack(side="left", fill="both", expand=False, padx=(0, 8))
        left.pack_propagate(False)

        # Columna derecha — consola de estado
        right = Frame(main, bg=C_BG)
        right.pack(side="left", fill="both", expand=True)

        self._build_files_panel(left)
        self._build_output_panel(left)
        self._build_actions_panel(left)
        self._build_console(right)

        # ── Status bar inferior ───────────────────────────────────────────────
        self.status_bar = Label(
            self.root, text="Listo — Seleccioná los tres archivos para comenzar",
            bg="#141824", fg=C_TEXT_MUTED,
            font=("Segoe UI", 9), anchor="w", padx=16
        )
        self.status_bar.pack(fill="x", side="bottom", ipady=6)

    # ── Panel de archivos ─────────────────────────────────────────────────────

    def _build_files_panel(self, parent):
        card = self._make_card(parent, "Archivos de entrada")

        # Archivo 1
        self._file_row(
            card, "Movimientos Bancarios",
            "Archivo con las 11 cuentas bancarias",
            self.path_movimientos,
            lambda: self._browse_file(self.path_movimientos, "Movimientos"),
            C_DD_SRL,
        )

        # Archivo 2
        self._file_row(
            card, "Saldos del Día",
            "Bancos del Día — control diario",
            self.path_saldos,
            lambda: self._browse_file(self.path_saldos, "Saldos del Día"),
            C_TEXT_MUTED,
        )

        # Archivo 3
        self._file_row(
            card, "Caja Fábrica Digital",
            "Registro mensual de caja",
            self.path_caja,
            lambda: self._browse_file(self.path_caja, "Caja"),
            C_D_CIA,
        )

    def _file_row(self, parent, title, subtitle, variable, command, accent_color):
        row = Frame(parent, bg=C_CARD, bd=0)
        row.pack(fill="x", pady=3)

        accent = Frame(row, bg=accent_color, width=3)
        accent.pack(side="left", fill="y")

        inner = Frame(row, bg=C_CARD, padx=10, pady=6)
        inner.pack(side="left", fill="x", expand=True)

        Label(inner, text=title, bg=C_CARD, fg=C_TEXT,
              font=("Segoe UI", 9, "bold")).pack(anchor="w")
        Label(inner, text=subtitle, bg=C_CARD, fg=C_TEXT_MUTED,
              font=("Segoe UI", 8)).pack(anchor="w")

        entry_row = Frame(inner, bg=C_CARD)
        entry_row.pack(fill="x", pady=(3, 0))

        entry = tk.Entry(
            entry_row, textvariable=variable,
            bg="#1A2035", fg=C_TEXT,
            insertbackground=C_TEXT,
            relief=FLAT, font=("Segoe UI", 8),
            highlightthickness=1,
            highlightbackground=C_BORDER,
            highlightcolor=C_ACCENT,
        )
        entry.pack(side="left", fill="x", expand=True, ipady=4)

        btn = tk.Button(
            entry_row, text="  Buscar  ",
            bg=C_ACCENT, fg="white",
            font=("Segoe UI", 8, "bold"),
            relief=FLAT, cursor="hand2",
            command=command,
            activebackground=C_BTN_HOVER,
            activeforeground="white",
            padx=6, pady=4,
        )
        btn.pack(side="right", padx=(4, 0))

    # ── Panel de salida ───────────────────────────────────────────────────────

    def _build_output_panel(self, parent):
        card = self._make_card(parent, "Carpeta de salida")

        row = Frame(card, bg=C_CARD)
        row.pack(fill="x", pady=3)

        entry = tk.Entry(
            row, textvariable=self.path_output,
            bg="#1A2035", fg=C_TEXT,
            insertbackground=C_TEXT,
            relief=FLAT, font=("Segoe UI", 8),
            highlightthickness=1,
            highlightbackground=C_BORDER,
            highlightcolor=C_ACCENT,
        )
        entry.pack(side="left", fill="x", expand=True, ipady=4)

        tk.Button(
            row, text="  Buscar  ",
            bg=C_CARD, fg=C_ACCENT,
            font=("Segoe UI", 8, "bold"),
            relief=FLAT, cursor="hand2",
            command=self._browse_output,
            highlightbackground=C_BORDER,
            highlightthickness=1,
            padx=6, pady=4,
        ).pack(side="right", padx=(4, 0))

    # ── Panel de acciones ─────────────────────────────────────────────────────

    def _build_actions_panel(self, parent):
        card = self._make_card(parent, "Acciones")

        # Botón principal
        self.btn_procesar = tk.Button(
            card,
            text="▶  PROCESAR Y GENERAR REPORTES",
            bg=C_ACCENT, fg="white",
            font=("Segoe UI", 11, "bold"),
            relief=FLAT, cursor="hand2",
            pady=12,
            command=self._run_process,
            activebackground=C_BTN_HOVER,
            activeforeground="white",
        )
        self.btn_procesar.pack(fill="x", pady=(0, 6))

        # Botón abrir carpeta salida
        self.btn_abrir = tk.Button(
            card,
            text="📁  Abrir carpeta de salida",
            bg=C_CARD, fg=C_ACCENT,
            font=("Segoe UI", 9),
            relief=FLAT, cursor="hand2",
            pady=7,
            command=self._open_output_folder,
            highlightbackground=C_BORDER,
            highlightthickness=1,
            state="disabled",
        )
        self.btn_abrir.pack(fill="x")

        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            card, variable=self.progress_var,
            maximum=100, mode="indeterminate",
            style="ARGUS.Horizontal.TProgressbar",
        )
        self._style_progressbar()
        self.progress_bar.pack(fill="x", pady=(8, 0))

    def _style_progressbar(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "ARGUS.Horizontal.TProgressbar",
            troughcolor=C_CARD,
            background=C_ACCENT,
            thickness=4,
        )

    # ── Consola de estado ─────────────────────────────────────────────────────

    def _build_console(self, parent):
        Label(
            parent, text="Estado del proceso",
            bg=C_BG, fg=C_TEXT_MUTED,
            font=("Segoe UI", 9, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 4))

        console_frame = Frame(parent, bg=C_BORDER, bd=1)
        console_frame.pack(fill="both", expand=True)

        self.console = Text(
            console_frame,
            bg="#0D1117", fg="#C9D1D9",
            font=("Consolas", 9),
            relief=FLAT, padx=12, pady=10,
            wrap="word",
            state="disabled",
            cursor="arrow",
        )

        scrollbar = ttk.Scrollbar(console_frame, command=self.console.yview)
        self.console.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.console.pack(fill="both", expand=True)

        # Tags de color para distintos tipos de mensaje
        self.console.tag_configure("info",    foreground="#58A6FF")
        self.console.tag_configure("success", foreground="#3FB950")
        self.console.tag_configure("warning", foreground="#D29922")
        self.console.tag_configure("error",   foreground="#F85149")
        self.console.tag_configure("dim",     foreground="#6E7681")
        self.console.tag_configure("bold",    foreground="#E6EDF3",
                                    font=("Consolas", 9, "bold"))

        # Mensaje inicial
        self._log("Sistema listo. Seleccioná los tres archivos Excel y presioná PROCESAR.", "dim")

    # ── Helpers de UI ─────────────────────────────────────────────────────────

    def _make_card(self, parent, title: str) -> Frame:
        wrapper = Frame(parent, bg=C_BG)
        wrapper.pack(fill="x", pady=(0, 10))
        Label(
            wrapper, text=title.upper(),
            bg=C_BG, fg=C_TEXT_MUTED,
            font=("Segoe UI", 8, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 4))
        card = Frame(wrapper, bg=C_CARD, padx=12, pady=10,
                     highlightbackground=C_BORDER, highlightthickness=1)
        card.pack(fill="x")
        return card

    def _log(self, msg: str, tag: str = "info"):
        """Escribe un mensaje en la consola."""
        self.console.configure(state="normal")
        self.console.insert(END, msg + "\n", tag)
        self.console.see(END)
        self.console.configure(state="disabled")

    def _clear_console(self):
        self.console.configure(state="normal")
        self.console.delete("1.0", END)
        self.console.configure(state="disabled")

    def _set_status(self, msg: str, color: str = C_TEXT_MUTED):
        self.status_bar.configure(text=msg, fg=color)

    # ── Explorador de archivos ────────────────────────────────────────────────

    def _browse_file(self, variable: StringVar, label: str):
        path = filedialog.askopenfilename(
            title=f"Seleccionar {label}",
            filetypes=[("Excel", "*.xlsx *.xlsm *.xls"), ("Todos", "*.*")],
        )
        if path:
            variable.set(path)
            self._log(f"✓ {label}: {Path(path).name}", "success")

    def _browse_output(self):
        path = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if path:
            self.path_output.set(path)

    def _open_output_folder(self):
        folder = self.path_output.get()
        if folder and Path(folder).exists():
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.run(["open", folder])
            else:
                subprocess.run(["xdg-open", folder])

    # ── Proceso principal ─────────────────────────────────────────────────────

    def _validate_inputs(self) -> bool:
        if not self.path_movimientos.get():
            messagebox.showerror("ARGUS", "Seleccioná el archivo de Movimientos Bancarios.")
            return False
        if not self.path_saldos.get():
            messagebox.showerror("ARGUS", "Seleccioná el archivo de Saldos del Día.")
            return False
        if not self.path_caja.get():
            messagebox.showerror("ARGUS", "Seleccioná el archivo de Caja Fábrica Digital.")
            return False
        if not self.path_output.get():
            messagebox.showerror("ARGUS", "Seleccioná una carpeta de salida.")
            return False
        return True

    def _run_process(self):
        if self._processing:
            return
        if not self._validate_inputs():
            return

        self._processing = True
        self._clear_console()
        self.btn_procesar.configure(text="⏳  Procesando...", state="disabled", bg="#2C4A6E")
        self.btn_abrir.configure(state="disabled")
        self.progress_bar.start(12)
        self._set_status("Procesando...", C_WARNING)

        def worker():
            try:
                result = self.processor.run(
                    path_movimientos = self.path_movimientos.get(),
                    path_saldos      = self.path_saldos.get(),
                    path_caja        = self.path_caja.get(),
                    output_folder    = self.path_output.get(),
                    on_progress      = lambda msg: self.root.after(0, self._log, msg, "info"),
                )
                self.root.after(0, self._on_complete, result)
            except Exception as e:
                logger.exception("Error inesperado en el procesamiento")
                self.root.after(0, self._on_error, str(e))

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def _on_complete(self, result):
        self.progress_bar.stop()
        self._processing = False

        if result.has_errors:
            for err in result.errors:
                self._log(f"✖ ERROR: {err}", "error")
            self.btn_procesar.configure(
                text="▶  PROCESAR Y GENERAR REPORTES",
                state="normal", bg=C_ACCENT
            )
            self._set_status("Error en el procesamiento — revisá los mensajes", C_ERROR)
            messagebox.showerror("ARGUS — Error", "\n".join(result.errors))
        else:
            if result.warnings:
                for w in result.warnings:
                    self._log(f"⚠ {w}", "warning")
            self._log(
                f"\n━━━ RESUMEN ━━━\n"
                f"  Pestañas procesadas : {result.sheets_processed}\n"
                f"  Transacciones       : {result.transactions_total}\n"
                f"  Cuentas resumidas   : {len(result.summaries)}\n"
                f"  Entradas de caja    : {len(result.caja_entries)}\n"
                f"  Archivos generados  : 3 Excel en carpeta de salida",
                "bold"
            )
            self.btn_procesar.configure(
                text="▶  PROCESAR Y GENERAR REPORTES",
                state="normal", bg=C_ACCENT
            )
            self.btn_abrir.configure(state="normal")
            self._set_status(
                f"✓ Completado — {result.transactions_total} transacciones procesadas",
                C_SUCCESS
            )

    def _on_error(self, error_msg: str):
        self.progress_bar.stop()
        self._processing = False
        self._log(f"✖ Error inesperado: {error_msg}", "error")
        self.btn_procesar.configure(
            text="▶  PROCESAR Y GENERAR REPORTES",
            state="normal", bg=C_ACCENT
        )
        self._set_status("Error inesperado — revisá los mensajes", C_ERROR)

    # ── Loop principal ────────────────────────────────────────────────────────

    def run(self):
        self.root.mainloop()

# main.py
# Punto de entrada de ARGUS — Automated Reconciliation & General Unified System
# Powered by McFlow

import logging
import sys
from pathlib import Path

# Asegurar que el directorio raíz esté en el path (necesario para PyInstaller)
ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Configurar logging
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_DIR / "argus.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("argus")


def main():
    logger.info("=" * 60)
    logger.info("ARGUS — Powered by McFlow  |  Iniciando...")
    logger.info("=" * 60)

    try:
        from app.ui.main_window import ArgusApp
        app = ArgusApp()
        app.run()
    except Exception as e:
        logger.exception(f"Error fatal al iniciar ARGUS: {e}")
        try:
            import tkinter.messagebox as mb
            mb.showerror(
                "ARGUS — Error Fatal",
                f"No se pudo iniciar la aplicación:\n\n{e}\n\n"
                f"Revisá el archivo logs/argus.log para más detalles."
            )
        except Exception:
            print(f"ERROR FATAL: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""Funciones utilitarias para la aplicacion"""

import logging
import sys
from pathlib import Path
from gi.repository import GLib
from .constants import APP_NAME


def get_app_data_path() -> Path:
    """Devuelve el directorio padre de usuario (XDG Standard) para los datos de la aplicacion"""

    path = Path(GLib.get_user_data_dir()) / APP_NAME

    try:
        path.mkdir(parents=True, exist_ok=True)
        return path
    except OSError as e:
        sys.stderr.write(f"CRITICAL: Falla al crear el repositorio de datos: {e}\n")
        sys.exit(1)


def setup_logging(base_path: Path):
    """Configurar sistema de logs"""

    log_file = base_path / "deepseek.log"
    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

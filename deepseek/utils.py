"""Funciones utilitarias para la aplicacion"""

import logging
from pathlib import Path


def setup_logging(base_path: Path):
    """Configurar sistema de logs"""

    log_file = base_path / "deepseek.log"
    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

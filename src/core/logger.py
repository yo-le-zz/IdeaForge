"""
IdeaForge — core/logger.py
Gestion des logs centralisée.
"""

import logging
import sys
from pathlib import Path

from core.config import LOG_FILE, APP_NAME


def get_logger(name: str = APP_NAME) -> logging.Logger:
    """
    Retourne un logger configuré avec :
    - Handler fichier (DEBUG+)
    - Handler console (WARNING+)
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        # Déjà configuré (évite les handlers dupliqués)
        return logger

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Handler fichier ──────────────────────────────────────────────────────
    try:
        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except OSError as exc:
        print(f"[WARN] Impossible de créer le fichier de log : {exc}", file=sys.stderr)

    # ── Handler console (uniquement WARNING et plus) ──────────────────────────
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logging.WARNING)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


# Logger global partagé
log = get_logger()

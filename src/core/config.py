"""
IdeaForge — core/config.py
Configuration centralisée du projet.
"""

import sys
import os
from pathlib import Path

# ── Import version depuis main ──────────────────────────────────────────────
# On remonte d'un niveau pour accéder à main.py (src/main.py)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import APP_VERSION, APP_VERSION_FULL, APP_NAME  # noqa: E402

# ── Chemins ─────────────────────────────────────────────────────────────────
# Quand compilé avec Nuitka, sys.frozen est défini
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parents[2]  # racine du projet

DATA_DIR       = BASE_DIR / "data"
QUESTIONS_FILE = DATA_DIR / "questions.json"
PROJECTS_FILE  = DATA_DIR / "projects.json"
LOG_FILE       = BASE_DIR / "ideaforge.log"

# ── Ollama ───────────────────────────────────────────────────────────────────
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL   = "mistral"          # Modèle par défaut (modifiable)
OLLAMA_TIMEOUT = 120                # Secondes avant timeout

# ── Limites ──────────────────────────────────────────────────────────────────
MAX_RETRIES_DUPLICATE = 5           # Tentatives avant abandon si doublon

# ── Création automatique du dossier data ──────────────────────────────────────
DATA_DIR.mkdir(parents=True, exist_ok=True)

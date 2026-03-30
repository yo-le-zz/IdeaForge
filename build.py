"""
IdeaForge — build.py
Script de compilation Nuitka pour Windows.

Usage :
    python build.py

Options Nuitka appliquées :
  - PAS de mode --onefile (dossier de sortie)
  - Icône : assets/icon.ico
  - Entrée : src/main.py
  - Sortie : dist/
  - Nom de l'exe : IdeaForge.exe
  - Nettoyage des dossiers temporaires après compilation
"""

import subprocess
import sys
import shutil
from pathlib import Path

# ── Import version depuis main ────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent / "src"))
from main import APP_NAME, APP_VERSION  # noqa: E402

# ── Chemins ───────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).parent.resolve()
SRC_ENTRY  = ROOT / "src" / "main.py"
ICON_PATH  = ROOT / "assets" / "icon.ico"
DIST_DIR   = ROOT / "dist"
BUILD_DIR  = ROOT / "build"          # Dossier temporaire Nuitka

EXE_NAME   = APP_NAME                # → IdeaForge.exe sur Windows


def run_nuitka() -> None:
    """Lance la compilation Nuitka avec les options configurées."""

    if not SRC_ENTRY.exists():
        print(f"[ERREUR] Fichier source introuvable : {SRC_ENTRY}")
        sys.exit(1)

    if not ICON_PATH.exists():
        print(f"[AVERTISSEMENT] Icône introuvable : {ICON_PATH} — compilation sans icône.")
        icon_args: list[str] = []
    else:
        icon_args = [f"--windows-icon-from-ico={ICON_PATH}"]

    DIST_DIR.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, "-m", "nuitka",
        # ── Mode : dossier (PAS --onefile) ───────────────────────────────────
        "--standalone",
        # ── Métadonnées exe ──────────────────────────────────────────────────
        f"--output-filename={EXE_NAME}",
        f"--product-name={APP_NAME}",
        f"--product-version={APP_VERSION}",
        f"--file-version={APP_VERSION}",
        f"--file-description={APP_NAME} — Générateur d'idées de projets IA",
        "--company-name=yo-le-zz",
        # ── Icône ────────────────────────────────────────────────────────────
        *icon_args,
        # ── Dossier de sortie ─────────────────────────────────────────────────
        f"--output-dir={DIST_DIR}",
        # ── Plugins nécessaires ───────────────────────────────────────────────
        "--enable-plugin=multiprocessing",
        # ── Inclusions explicites (modules dynamiques) ────────────────────────
        "--include-package=textual",
        "--include-package=core",
        "--include-package=ui",
        # ── Dossier build temporaire ──────────────────────────────────────────
        f"--build-dir={BUILD_DIR}",
        # ── Console (CLI) — retirer pour une app sans fenêtre console ─────────
        "--windows-console-mode=attach",
        # ── Source ────────────────────────────────────────────────────────────
        str(SRC_ENTRY),
    ]

    print(f"\n{'='*60}")
    print(f"  {APP_NAME} {APP_VERSION} — Compilation Nuitka")
    print(f"{'='*60}")
    print(f"  Source  : {SRC_ENTRY}")
    print(f"  Sortie  : {DIST_DIR}")
    print(f"  Icône   : {ICON_PATH if ICON_PATH.exists() else '(absente)'}")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd, check=False)

    # ── Nettoyage des dossiers temporaires ────────────────────────────────────
    _cleanup()

    if result.returncode != 0:
        print(f"\n[ERREUR] Nuitka a échoué (code {result.returncode}).")
        print("Vérifiez que Nuitka est installé : pip install nuitka")
        sys.exit(result.returncode)

    print(f"\n[OK] Compilation terminée → {DIST_DIR}")


def _cleanup() -> None:
    """Supprime les dossiers temporaires générés par Nuitka."""
    targets = [BUILD_DIR]

    # Nuitka crée parfois un dossier *.build dans le répertoire courant
    for p in ROOT.glob("*.build"):
        targets.append(p)
    for p in ROOT.glob("*.dist"):
        # Ne pas supprimer notre dist/ de sortie !
        if p.resolve() != DIST_DIR.resolve():
            targets.append(p)

    for t in targets:
        if t.exists():
            shutil.rmtree(t, ignore_errors=True)
            print(f"  [nettoyage] Supprimé : {t}")


if __name__ == "__main__":
    run_nuitka()

"""
IdeaForge - Main Entry Point
Outil CLI interactif de génération d'idées de projets informatiques via IA locale.

Auteur : yo-le-zz
Licence : IdeaForge License (voir LICENSE)
"""

import sys
import argparse

# ─────────────────────────────────────────────
# VERSION — source unique de vérité
# Utilisée partout dans le projet via import
# ─────────────────────────────────────────────
APP_VERSION_FULL = "V1.0.0"   # Affichage lisible (ex: banner, UI)
APP_VERSION      = "1.0.0"    # Semver pur (ex: --version, packaging)
APP_NAME         = "IdeaForge"

def parse_args() -> argparse.Namespace:
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=f"{APP_NAME} {APP_VERSION_FULL} — Génération d'idées de projets via IA locale",
        add_help=True,
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Affiche la version et quitte",
    )
    return parser.parse_args()


def main() -> None:
    """Point d'entrée principal."""
    args = parse_args()

    # ── --version : afficher et quitter immédiatement ──
    if args.version:
        print(APP_VERSION)
        sys.exit(0)

    # ── Lancement de l'application Textual ──
    try:
        from ui.app import IdeaForgeApp
        app = IdeaForgeApp()
        app.run()
    except ImportError as exc:
        print(f"[ERREUR] Dépendance manquante : {exc}")
        print("Installez les dépendances : pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAu revoir !")
        sys.exit(0)


if __name__ == "__main__":
    main()

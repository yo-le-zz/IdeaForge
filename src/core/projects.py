"""
IdeaForge — core/projects.py
Gestion du stockage et de la déduplication des projets générés.

Schéma d'un projet :
{
    "name":        str — Nom du projet
    "description": str — Description courte
    "language":    str — Langage recommandé
    "details":     str — Explication concrète du fonctionnement
}
"""

from __future__ import annotations

import json
from typing import Any

from core.config import PROJECTS_FILE
from core.logger import log


# ── Helpers ──────────────────────────────────────────────────────────────────

def _load_raw() -> list[dict[str, Any]]:
    """Charge projects.json, retourne [] si absent/corrompu."""
    if not PROJECTS_FILE.exists():
        return []
    try:
        text = PROJECTS_FILE.read_text(encoding="utf-8").strip()
        if not text:
            return []
        data = json.loads(text)
        if not isinstance(data, list):
            log.warning("projects.json ne contient pas une liste — réinitialisation.")
            return []
        return data
    except json.JSONDecodeError as exc:
        log.error("projects.json corrompu : %s — réinitialisation.", exc)
        return []


def _save(projects: list[dict[str, Any]]) -> None:
    """Persiste la liste dans projects.json."""
    PROJECTS_FILE.write_text(
        json.dumps(projects, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    log.debug("projects.json sauvegardé (%d projet(s)).", len(projects))


# ── API publique ──────────────────────────────────────────────────────────────

def load_projects() -> list[dict[str, Any]]:
    """Retourne tous les projets stockés."""
    return _load_raw()


def save_project(project: dict[str, Any]) -> None:
    """Ajoute un projet à la liste persistée."""
    required = {"name", "description", "language", "details"}
    missing = required - project.keys()
    if missing:
        raise ValueError(f"Champs manquants dans le projet : {missing}")

    projects = _load_raw()
    projects.append(project)
    _save(projects)
    log.info("Projet sauvegardé : %s", project.get("name"))


def is_duplicate(project: dict[str, Any]) -> bool:
    """
    Vérifie si un projet est un doublon.

    La comparaison est faite sur le nom normalisé (minuscules, sans espaces).
    """
    existing = _load_raw()
    new_name = _normalize(project.get("name", ""))

    for p in existing:
        if _normalize(p.get("name", "")) == new_name:
            log.info("Doublon détecté : '%s'", project.get("name"))
            return True
    return False


def get_project_names() -> list[str]:
    """Retourne uniquement les noms des projets existants."""
    return [p.get("name", "") for p in _load_raw()]


def _normalize(name: str) -> str:
    """Normalise un nom pour la comparaison (minuscules, sans espaces)."""
    return name.lower().replace(" ", "").strip()

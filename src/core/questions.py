"""
IdeaForge — core/questions.py
Gestion CRUD des questions depuis questions.json.

Schéma d'une question :
{
    "id":         str   — identifiant unique (UUID)
    "texte":      str   — libellé affiché à l'utilisateur
    "type":       str   — "choix" | "texte"
    "options":    list  — liste d'options (uniquement si type == "choix")
    "multi":      bool  — choix multiples autorisés (uniquement si type == "choix")
    "max_length": int   — longueur max de la réponse (uniquement si type == "texte")
}
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from core.config import QUESTIONS_FILE
from core.logger import log


# ── Helpers ──────────────────────────────────────────────────────────────────

def _load_raw() -> list[dict[str, Any]]:
    """Charge le JSON brut depuis le fichier, retourne [] si absent/corrompu."""
    if not QUESTIONS_FILE.exists():
        log.info("questions.json introuvable — initialisation vide.")
        return []
    try:
        text = QUESTIONS_FILE.read_text(encoding="utf-8").strip()
        if not text:
            return []
        data = json.loads(text)
        if not isinstance(data, list):
            log.warning("questions.json ne contient pas une liste — réinitialisation.")
            return []
        return data
    except json.JSONDecodeError as exc:
        log.error("questions.json corrompu : %s — réinitialisation.", exc)
        return []


def _save(questions: list[dict[str, Any]]) -> None:
    """Persiste la liste de questions dans le fichier JSON."""
    QUESTIONS_FILE.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    log.debug("questions.json sauvegardé (%d question(s)).", len(questions))


# ── API publique ──────────────────────────────────────────────────────────────

def load_questions() -> list[dict[str, Any]]:
    """Retourne la liste complète des questions."""
    return _load_raw()


def add_question(
    texte: str,
    type_: str,
    options: list[str] | None = None,
    multi: bool = False,
    max_length: int = 200,
) -> dict[str, Any]:
    """
    Crée et ajoute une nouvelle question.

    Args:
        texte:      Libellé de la question.
        type_:      "choix" ou "texte".
        options:    Liste d'options (type == "choix" uniquement).
        multi:      Autorise la sélection multiple.
        max_length: Longueur maximale (type == "texte" uniquement).

    Returns:
        La question créée.
    """
    if type_ not in ("choix", "texte"):
        raise ValueError(f"Type invalide '{type_}' — attendu 'choix' ou 'texte'.")

    question: dict[str, Any] = {
        "id":   str(uuid.uuid4()),
        "texte": texte.strip(),
        "type": type_,
    }

    if type_ == "choix":
        question["options"] = options or []
        question["multi"]   = multi
    else:
        question["max_length"] = max_length

    questions = _load_raw()
    questions.append(question)
    _save(questions)
    log.info("Question ajoutée : %s (%s)", question["id"], texte)
    return question


def update_question(question_id: str, **kwargs: Any) -> bool:
    """
    Met à jour les champs d'une question existante.

    Args:
        question_id: ID de la question à modifier.
        **kwargs:    Champs à mettre à jour.

    Returns:
        True si trouvée et modifiée, False sinon.
    """
    questions = _load_raw()
    for q in questions:
        if q["id"] == question_id:
            for key, value in kwargs.items():
                q[key] = value
            _save(questions)
            log.info("Question mise à jour : %s", question_id)
            return True
    log.warning("Question introuvable pour mise à jour : %s", question_id)
    return False


def delete_question(question_id: str) -> bool:
    """
    Supprime une question par son ID.

    Returns:
        True si supprimée, False si introuvable.
    """
    questions = _load_raw()
    new_list = [q for q in questions if q["id"] != question_id]
    if len(new_list) == len(questions):
        log.warning("Question introuvable pour suppression : %s", question_id)
        return False
    _save(new_list)
    log.info("Question supprimée : %s", question_id)
    return True


def has_questions() -> bool:
    """Retourne True si au moins une question est définie."""
    return bool(_load_raw())

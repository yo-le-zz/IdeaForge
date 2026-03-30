"""
IdeaForge — core/ollama_client.py
Intégration avec Ollama (API locale HTTP).

Génère une idée de projet UNIQUE en JSON strict à partir :
- des réponses utilisateur
- de la liste des projets déjà générés (anti-doublon côté prompt)
"""

from __future__ import annotations

import json
import urllib.request
import urllib.error
from typing import Any

from core.config import OLLAMA_API_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT, MAX_RETRIES_DUPLICATE
from core.logger import log
from core.projects import is_duplicate, save_project


# ── Prompt ────────────────────────────────────────────────────────────────────

def _build_prompt(answers: dict[str, Any], existing_names: list[str]) -> str:
    """Construit le prompt envoyé à Ollama."""

    answers_block = "\n".join(
        f"  - {qid}: {value}" for qid, value in answers.items()
    )

    existing_block = (
        "\n".join(f"  - {name}" for name in existing_names)
        if existing_names
        else "  (aucun projet existant)"
    )

    return f"""Tu es un expert en ingénierie logicielle créatif.

À partir des préférences suivantes de l'utilisateur, génère UNE idée de projet informatique ORIGINALE et UNIQUE.

=== PRÉFÉRENCES UTILISATEUR ===
{answers_block}

=== PROJETS DÉJÀ GÉNÉRÉS (À ÉVITER ABSOLUMENT) ===
{existing_block}

=== RÈGLES STRICTES ===
1. L'idée doit être DIFFÉRENTE de tous les projets listés ci-dessus.
2. L'idée doit correspondre aux préférences de l'utilisateur.
3. Tu dois répondre UNIQUEMENT avec un objet JSON valide, sans texte avant ni après.
4. Le JSON doit respecter EXACTEMENT ce format :

{{
  "name": "Nom du projet",
  "description": "Description courte en une phrase",
  "language": "Langage ou technologie principale recommandée",
  "details": "Explication concrète du fonctionnement du projet en 3-5 phrases"
}}

Réponds maintenant avec le JSON uniquement :"""


# ── Appel API Ollama ──────────────────────────────────────────────────────────

def _call_ollama(prompt: str) -> str:
    """
    Envoie un prompt à l'API Ollama et retourne la réponse brute.

    Raises:
        ConnectionError: Si Ollama est inaccessible.
        RuntimeError:    En cas d'erreur HTTP ou de timeout.
    """
    payload = json.dumps({
        "model":  OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(
        url=OLLAMA_API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            return data.get("response", "")
    except urllib.error.URLError as exc:
        raise ConnectionError(
            f"Ollama inaccessible ({OLLAMA_API_URL}). "
            f"Assurez-vous qu'Ollama est lancé. Détail : {exc}"
        ) from exc
    except TimeoutError as exc:
        raise RuntimeError(f"Timeout lors de l'appel Ollama ({OLLAMA_TIMEOUT}s).") from exc


def _parse_project_json(raw: str) -> dict[str, Any]:
    """
    Extrait et valide le JSON de la réponse de l'IA.

    Raises:
        ValueError: Si le JSON est absent ou mal formé.
    """
    # Cherche le premier '{' et le dernier '}' pour extraire le JSON même si
    # l'IA ajoute du texte parasite avant/après.
    start = raw.find("{")
    end   = raw.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(f"Aucun JSON trouvé dans la réponse : {raw[:200]!r}")

    json_str = raw[start: end + 1]

    try:
        project = json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON malformé : {exc}\nRéponse brute : {json_str[:300]!r}") from exc

    required = {"name", "description", "language", "details"}
    missing  = required - project.keys()
    if missing:
        raise ValueError(f"Champs manquants dans le JSON de l'IA : {missing}")

    return project


# ── API publique ──────────────────────────────────────────────────────────────

def generate_project_idea(
    answers: dict[str, Any],
    existing_projects: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Génère une idée de projet UNIQUE via Ollama.

    Relance automatiquement jusqu'à MAX_RETRIES_DUPLICATE fois si doublon.

    Args:
        answers:           Réponses utilisateur {question_id: valeur}.
        existing_projects: Liste des projets déjà générés.

    Returns:
        Un dict projet valide et non-doublon.

    Raises:
        ConnectionError: Si Ollama est inaccessible.
        RuntimeError:    Si trop de doublons consécutifs.
    """
    existing_names = [p.get("name", "") for p in existing_projects]

    for attempt in range(1, MAX_RETRIES_DUPLICATE + 1):
        log.info("Génération tentative %d/%d…", attempt, MAX_RETRIES_DUPLICATE)

        prompt  = _build_prompt(answers, existing_names)
        raw     = _call_ollama(prompt)

        log.debug("Réponse brute Ollama : %s", raw[:300])

        try:
            project = _parse_project_json(raw)
        except ValueError as exc:
            log.warning("Réponse invalide (tentative %d) : %s", attempt, exc)
            continue

        if is_duplicate(project):
            log.info("Doublon détecté, nouvelle tentative…")
            # Ajouter le nom doublon à la liste pour l'éviter dans le prochain prompt
            existing_names.append(project["name"])
            continue

        # Projet valide et unique ✓
        log.info("Projet généré avec succès : %s", project["name"])
        return project

    raise RuntimeError(
        f"Impossible de générer un projet unique après {MAX_RETRIES_DUPLICATE} tentatives. "
        "Essayez de changer vos réponses ou d'utiliser un modèle différent."
    )


def check_ollama_available() -> bool:
    """Vérifie rapidement si Ollama répond (ping léger)."""
    try:
        req = urllib.request.Request(
            url="http://localhost:11434/",
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=3):
            return True
    except Exception:
        return False

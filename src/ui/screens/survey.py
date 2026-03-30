"""
IdeaForge — ui/screens/survey.py
Écran de réponse aux questions.

Génère dynamiquement les widgets selon le type de chaque question :
- type "choix" + multi=True   → Checkboxes
- type "choix" + multi=False  → RadioSet
- type "texte"                → Input avec limite max_length
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Button, Checkbox, Footer, Input, Label,
    RadioButton, RadioSet, Static,
)
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual import on

import re

from core.questions import load_questions
from core.logger import log


class SurveyScreen(Screen):
    """Formulaire de réponse aux questions définies."""

    def __init__(self) -> None:
        super().__init__()
        self._questions: list[dict] = []

    # ── Composition ──────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        self._questions = load_questions()

        yield Static("📝  Répondez aux questions", classes="title")
        yield Static(
            "Vos réponses guideront l'IA pour générer une idée de projet unique.",
            classes="subtitle",
        )

        with ScrollableContainer(id="survey_scroll"):
            for idx, q in enumerate(self._questions, 1):
                yield self._build_question_widget(idx, q)

        with Horizontal(classes="toolbar"):
            yield Button("← Annuler", id="btn_cancel")
            yield Button("✨ Générer l'idée", id="btn_generate", classes="primary")

        yield Footer()

    # ── Construction dynamique des widgets ───────────────────────────────────

    def _build_question_widget(self, idx: int, q: dict) -> Vertical:
        """Construit le widget adapté au type de question."""
        q_id  = q["id"]
        texte = q["texte"]
        type_ = q["type"]

        # Rassemble les enfants dans une liste ordinaire
        children: list = [Label(f"{idx}. {texte}", classes="section-title")]

        if type_ == "choix":
            options = q.get("options", [])
            multi   = q.get("multi", False)

            if multi:
                for opt in options:
                    # Remplace tout caractère non alphanumérique par "_" (IDs Textual : [a-zA-Z0-9_-] uniquement)
                    safe_opt = re.sub(r"[^a-zA-Z0-9]", "_", opt)
                    children.append(Checkbox(opt, id=f"chk_{q_id}_{safe_opt}"))
            else:
                buttons = [RadioButton(opt) for opt in options]
                children.append(RadioSet(*buttons, id=f"radio_{q_id}"))

        elif type_ == "texte":
            max_len = q.get("max_length", 200)
            children.append(Input(
                placeholder=f"Votre réponse (max {max_len} caractères)…",
                max_length=max_len,
                id=f"inp_{q_id}",
            ))

        # On passe les enfants directement au constructeur Vertical
        return Vertical(*children, classes="card", id=f"widget_{q_id}")

    # ── Collecte des réponses ────────────────────────────────────────────────

    def _collect_answers(self) -> dict[str, object]:
        """
        Parcourt tous les widgets et retourne un dict {question_id: réponse}.
        """
        answers: dict[str, object] = {}

        for q in self._questions:
            q_id  = q["id"]
            type_ = q["type"]

            if type_ == "choix":
                multi = q.get("multi", False)

                if multi:
                    # Récupère toutes les checkboxes cochées pour cette question
                    selected: list[str] = []
                    for opt in q.get("options", []):
                        safe_opt = re.sub(r"[^a-zA-Z0-9]", "_", opt)
                        try:
                            chk = self.query_one(f"#chk_{q_id}_{safe_opt}", Checkbox)
                            if chk.value:
                                selected.append(opt)
                        except Exception:
                            pass
                    answers[q_id] = selected if selected else ["(aucun choix)"]

                else:
                    # RadioSet : récupère l'option sélectionnée
                    try:
                        rs = self.query_one(f"#radio_{q_id}", RadioSet)
                        options = q.get("options", [])
                        idx = rs.pressed_index
                        answers[q_id] = options[idx] if idx is not None and idx < len(options) else "(aucun)"
                    except Exception:
                        answers[q_id] = "(aucun)"

            elif type_ == "texte":
                try:
                    inp = self.query_one(f"#inp_{q_id}", Input)
                    answers[q_id] = inp.value.strip() or "(vide)"
                except Exception:
                    answers[q_id] = "(vide)"

        return answers

    # ── Événements ───────────────────────────────────────────────────────────

    @on(Button.Pressed, "#btn_cancel")
    def action_cancel(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, "#btn_generate")
    def action_generate(self) -> None:
        """Valide les réponses et lance l'écran de génération."""
        answers = self._collect_answers()
        log.info("Réponses collectées : %s", answers)

        # Enrichit les réponses avec les textes des questions (pour le prompt)
        answers_labeled: dict[str, str] = {}
        for q in self._questions:
            q_id = q["id"]
            key  = q["texte"]
            val  = answers.get(q_id, "(non répondu)")
            if isinstance(val, list):
                val = ", ".join(val)
            answers_labeled[key] = val

        from ui.screens.generating import GeneratingScreen
        self.app.push_screen(GeneratingScreen(answers_labeled))
"""
IdeaForge — ui/screens/generating.py
Écran de génération en cours (thread d'arrière-plan + spinner).
"""

from __future__ import annotations

import threading
from typing import Any

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, LoadingIndicator, Static
from textual.containers import Center, Vertical
from textual import on, work

from core.ollama_client import generate_project_idea
from core.projects import load_projects, save_project
from core.logger import log


class GeneratingScreen(Screen):
    """Écran affiché pendant la génération d'un projet."""

    def __init__(self, answers: dict[str, Any]) -> None:
        super().__init__()
        self._answers   = answers
        self._result:   dict | None = None
        self._error:    str  | None = None

    # ── Composition ──────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        yield Static("✨  Génération en cours…", classes="title")
        yield Static(
            "L'IA locale analyse vos préférences et cherche une idée unique…",
            classes="subtitle",
        )

        with Center():
            yield LoadingIndicator()

        with Center():
            yield Label("", id="status_label", classes="muted")

        with Center():
            yield Button("✕ Annuler", id="btn_cancel", classes="danger")

        yield Footer()

    # ── Démarrage automatique ─────────────────────────────────────────────────

    def on_mount(self) -> None:
        """Lance le thread de génération dès que l'écran est monté."""
        self._generate_async()

    # ── Thread de génération ─────────────────────────────────────────────────

    def _generate_async(self) -> None:
        """Lance la génération dans un thread pour ne pas bloquer l'UI."""
        def _worker() -> None:
            try:
                self.call_from_thread(
                    self.query_one("#status_label", Label).update,
                    "Connexion à Ollama…",
                )
                existing = load_projects()
                self.call_from_thread(
                    self.query_one("#status_label", Label).update,
                    "Génération de l'idée (peut prendre jusqu'à 2 min)…",
                )
                project = generate_project_idea(self._answers, existing)
                self._result = project
                self.call_from_thread(self._on_success, project)
            except Exception as exc:
                self._error = str(exc)
                log.error("Erreur génération : %s", exc)
                self.call_from_thread(self._on_error, str(exc))

        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    # ── Callbacks (appelés depuis le thread via call_from_thread) ─────────────

    def _on_success(self, project: dict) -> None:
        """Appelé quand la génération réussit."""
        try:
            save_project(project)
            log.info("Projet sauvegardé : %s", project.get("name"))
        except Exception as exc:
            log.error("Erreur sauvegarde : %s", exc)

        from ui.screens.result import ResultScreen
        # switch_screen remplace l'écran courant (generating) sans empiler
        self.app.switch_screen(ResultScreen(project))

    def _on_error(self, message: str) -> None:
        """Appelé en cas d'erreur."""
        from ui.screens.error_screen import ErrorScreen
        self.app.switch_screen(ErrorScreen(f"Erreur lors de la génération :\n\n{message}"))

    # ── Événements ───────────────────────────────────────────────────────────

    @on(Button.Pressed, "#btn_cancel")
    def action_cancel(self) -> None:
        """Annule et revient au survey (un seul pop)."""
        self.app.pop_screen()
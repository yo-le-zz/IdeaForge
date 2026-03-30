"""
IdeaForge — ui/screens/welcome.py
Écran d'accueil : status Ollama + navigation principale.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, Static
from textual.containers import Center, Vertical

from core.config import APP_NAME, APP_VERSION_FULL, OLLAMA_MODEL
from core.ollama_client import check_ollama_available
from core.questions import has_questions
from core.projects import load_projects
from core.logger import log


BANNER = r"""
  ___    _             _____
 |_ _|  | |   ___  __ |  ___|  ___   _ __   __ _   ___
  | |   | |  / _ \/ _` | |_   / _ \ | '__| / _` | / _ \
  | |   | | |  __/ (_| |  _| | (_) || |   | (_| ||  __/
 |___|  |_|  \___|\__,_|_|    \___/ |_|    \__, | \___|
                                            |___/
"""


class WelcomeScreen(Screen):
    """Écran d'accueil principal."""

    BINDINGS = [("q", "app.quit", "Quitter")]

    def compose(self) -> ComposeResult:
        ollama_ok = check_ollama_available()
        q_count   = len(__import__("core.questions", fromlist=["load_questions"]).load_questions())
        p_count   = len(load_projects())

        status_cls  = "success" if ollama_ok else "error"
        status_text = (
            f"✓ Ollama en ligne — modèle : {OLLAMA_MODEL}"
            if ollama_ok
            else "✗ Ollama hors ligne — lancez Ollama avant de continuer"
        )

        yield Static(BANNER, classes="title")
        yield Static(f"{APP_NAME} {APP_VERSION_FULL}", classes="title")
        yield Static("Générateur d'idées de projets informatiques par IA locale", classes="subtitle")

        with Center():
            with Vertical(classes="card"):
                yield Label(status_text, classes=status_cls)
                yield Static(f"  Questions définies : {q_count}", classes="muted")
                yield Static(f"  Projets générés    : {p_count}", classes="muted")

        with Center():
            with Vertical():
                yield Button("▶  Générer une idée", id="btn_generate", classes="primary")
                yield Button("⚙  Gérer les questions", id="btn_questions")
                yield Button("📋 Voir les projets", id="btn_projects")
                yield Button("✕  Quitter", id="btn_quit", classes="danger")

        yield Footer()

    # ── Événements ────────────────────────────────────────────────────────────

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id

        if btn_id == "btn_generate":
            self._start_generate()
        elif btn_id == "btn_questions":
            from ui.screens.question_manager import QuestionManagerScreen
            self.app.push_screen(QuestionManagerScreen())
        elif btn_id == "btn_projects":
            from ui.screens.projects_list import ProjectsListScreen
            self.app.push_screen(ProjectsListScreen())
        elif btn_id == "btn_quit":
            self.app.exit()

    def _start_generate(self) -> None:
        """Lance le formulaire ou propose de créer des questions d'abord."""
        if not has_questions():
            from ui.screens.question_manager import QuestionManagerScreen
            self.app.push_screen(
                QuestionManagerScreen(message="Aucune question définie. Créez-en d'abord !")
            )
            return

        if not check_ollama_available():
            self.app.push_screen(
                __import__("ui.screens.error_screen", fromlist=["ErrorScreen"]).ErrorScreen(
                    "Ollama est hors ligne.\n\nLancez Ollama avec :\n  ollama serve\n\n"
                    f"Et assurez-vous que le modèle '{OLLAMA_MODEL}' est disponible :\n"
                    f"  ollama pull {OLLAMA_MODEL}"
                )
            )
            return

        from ui.screens.survey import SurveyScreen
        self.app.push_screen(SurveyScreen())

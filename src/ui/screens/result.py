"""
IdeaForge — ui/screens/result.py
Écran d'affichage du projet généré.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, Static
from textual.containers import Center, Horizontal, ScrollableContainer, Vertical
from textual import on


class ResultScreen(Screen):
    """Affiche le projet généré et propose de recommencer ou de quitter."""

    def __init__(self, project: dict) -> None:
        super().__init__()
        self._project = project

    # ── Composition ──────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        p = self._project

        yield Static("🎉  Idée générée avec succès !", classes="title")

        with ScrollableContainer():
            with Vertical(classes="card"):
                yield Label("Nom du projet", classes="muted")
                yield Static(p.get("name", "—"), classes="success")

            with Vertical(classes="card"):
                yield Label("Description", classes="muted")
                yield Static(p.get("description", "—"))

            with Vertical(classes="card"):
                yield Label("Langage / Technologie", classes="muted")
                yield Static(f"🛠  {p.get('language', '—')}", classes="section-title")

            with Vertical(classes="card"):
                yield Label("Détails du projet", classes="muted")
                yield Static(p.get("details", "—"))

        with Horizontal(classes="toolbar"):
            yield Button("🔄 Générer une autre idée", id="btn_again", classes="primary")
            yield Button("📋 Voir tous les projets", id="btn_projects")
            yield Button("🏠 Accueil", id="btn_home")

        yield Footer()

    # ── Événements ───────────────────────────────────────────────────────────

    @on(Button.Pressed, "#btn_again")
    def action_again(self) -> None:
        """Relance le formulaire sans repasser par l'accueil."""
        from ui.screens.survey import SurveyScreen
        self.app.switch_screen(SurveyScreen())

    @on(Button.Pressed, "#btn_projects")
    def action_projects(self) -> None:
        from ui.screens.projects_list import ProjectsListScreen
        self.app.push_screen(ProjectsListScreen())

    @on(Button.Pressed, "#btn_home")
    def action_home(self) -> None:
        """Vide la pile et revient à l'accueil."""
        from ui.screens.welcome import WelcomeScreen
        self.app.switch_screen(WelcomeScreen())

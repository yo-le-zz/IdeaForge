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
        """Pop result+generating+survey, puis push un nouveau survey."""
        # La pile est : welcome > survey > generating > result (switch)
        # result a remplacé generating via switch_screen, donc pile : welcome > survey > result
        # On pop result (retour survey), puis on switch survey par un nouveau
        self.app.pop_screen()   # → retour sur survey
        from ui.screens.survey import SurveyScreen
        self.app.switch_screen(SurveyScreen())  # remplace le vieux survey

    @on(Button.Pressed, "#btn_projects")
    def action_projects(self) -> None:
        from ui.screens.projects_list import ProjectsListScreen
        self.app.push_screen(ProjectsListScreen())

    @on(Button.Pressed, "#btn_home")
    def action_home(self) -> None:
        """Revient à l'accueil en vidant toute la pile sauf welcome."""
        # Pile actuelle : welcome > survey > result
        self.app.pop_screen()  # pop result → survey
        self.app.pop_screen()  # pop survey → welcome
"""
IdeaForge — ui/screens/error_screen.py
Écran générique d'affichage d'erreur.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Static
from textual.containers import Center, Vertical
from textual import on


class ErrorScreen(Screen):
    """Affiche un message d'erreur et propose de retourner à l'accueil."""

    def __init__(self, message: str) -> None:
        super().__init__()
        self._message = message

    def compose(self) -> ComposeResult:
        yield Static("⚠  Erreur", classes="title")

        with Center():
            with Vertical(classes="card"):
                yield Static(self._message, classes="error")

        with Center():
            yield Button("← Retour", id="btn_back", classes="primary")

        yield Footer()

    @on(Button.Pressed, "#btn_back")
    def action_back(self) -> None:
        self.app.pop_screen()

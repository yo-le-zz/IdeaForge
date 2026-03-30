"""
IdeaForge — ui/app.py
Application Textual principale.

Orchestre les différents écrans :
  - WelcomeScreen    → accueil + vérification Ollama
  - QuestionManagerScreen → gestion CRUD des questions
  - SurveyScreen     → formulaire de réponse aux questions
  - GeneratingScreen → génération en cours (thread)
  - ResultScreen     → affichage du projet généré
"""

from __future__ import annotations

import sys
from pathlib import Path

# Assure que src/ est dans le path (utile en mode compilé ou direct)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from textual.app import App, ComposeResult
from textual.binding import Binding

from core.config import APP_NAME, APP_VERSION_FULL  # type: ignore
from core.logger import log


class IdeaForgeApp(App):
    """Application principale IdeaForge."""

    TITLE    = f"{APP_NAME} {APP_VERSION_FULL}"
    SUB_TITLE = "Générateur d'idées de projets par IA locale"

    CSS = """
    /* ── Palette globale ─────────────────────────────────────────────── */
    $bg:         #0d1117;
    $surface:    #161b22;
    $border:     #30363d;
    $accent:     #58a6ff;
    $accent2:    #3fb950;
    $warn:       #d29922;
    $error:      #f85149;
    $text:       #c9d1d9;
    $text-muted: #8b949e;

    Screen {
        background: $bg;
        color: $text;
    }

    /* ── Titres / labels ─────────────────────────────────────────────── */
    .title {
        text-style: bold;
        color: $accent;
        text-align: center;
        margin-bottom: 1;
    }
    .subtitle {
        color: $text-muted;
        text-align: center;
        margin-bottom: 2;
    }
    .section-title {
        text-style: bold;
        color: $accent2;
        margin: 1 0;
    }
    .muted {
        color: $text-muted;
    }
    .success {
        color: $accent2;
        text-style: bold;
    }
    .error {
        color: $error;
        text-style: bold;
    }
    .warn {
        color: $warn;
    }

    /* ── Boutons ─────────────────────────────────────────────────────── */
    Button {
        margin: 0 1;
    }
    Button.primary {
        background: $accent;
        color: #000000;
        text-style: bold;
    }
    Button.danger {
        background: $error;
        color: #ffffff;
    }
    Button.success {
        background: $accent2;
        color: #000000;
        text-style: bold;
    }

    /* ── Inputs ──────────────────────────────────────────────────────── */
    Input {
        background: $surface;
        border: solid $border;
        color: $text;
    }
    Input:focus {
        border: solid $accent;
    }
    TextArea {
        background: $surface;
        border: solid $border;
        color: $text;
        height: 5;
    }
    TextArea:focus {
        border: solid $accent;
    }

    /* ── Listes / scrollables ────────────────────────────────────────── */
    ListView {
        background: $surface;
        border: solid $border;
        height: 1fr;
    }
    ListItem {
        color: $text;
        padding: 0 1;
    }
    ListItem:hover {
        background: $border;
    }
    ListItem.--highlight {
        background: $accent;
        color: #000000;
    }

    /* ── Conteneurs ──────────────────────────────────────────────────── */
    .card {
        background: $surface;
        border: solid $border;
        padding: 1 2;
        margin: 1 0;
    }
    .toolbar {
        height: 3;
        dock: bottom;
        background: $surface;
        border-top: solid $border;
        align: center middle;
    }
    .center {
        align: center middle;
    }
    .row {
        layout: horizontal;
        height: auto;
    }

    /* ── Checkbox ────────────────────────────────────────────────────── */
    Checkbox {
        background: $bg;
        color: $text;
    }
    Checkbox:focus {
        background: $surface;
    }

    /* ── RadioSet ────────────────────────────────────────────────────── */
    RadioSet {
        background: $bg;
        border: solid $border;
        padding: 0 1;
    }
    RadioButton {
        color: $text;
    }

    /* ── Select ──────────────────────────────────────────────────────── */
    Select {
        background: $surface;
        border: solid $border;
    }

    /* ── ProgressBar ─────────────────────────────────────────────────── */
    ProgressBar {
        color: $accent;
    }

    /* ── Footer ──────────────────────────────────────────────────────── */
    Footer {
        background: $surface;
        color: $text-muted;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quitter", show=True),
    ]

    def on_mount(self) -> None:
        """Lance l'écran d'accueil au démarrage."""
        from ui.screens.welcome import WelcomeScreen
        self.push_screen(WelcomeScreen())
        log.info("IdeaForge démarré.")

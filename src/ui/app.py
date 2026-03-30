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
        layers: base overlay;
    }

    /* ── Titres / labels ─────────────────────────────────────────────── */
    .title {
        text-style: bold;
        color: $accent;
        text-align: center;
        height: auto;
        margin-bottom: 1;
    }
    .subtitle {
        color: $text-muted;
        text-align: center;
        height: auto;
        margin-bottom: 1;
    }
    .section-title {
        text-style: bold;
        color: $accent2;
        height: auto;
        margin: 0 0 1 0;
    }
    .muted {
        color: $text-muted;
        height: auto;
    }
    .success {
        color: $accent2;
        text-style: bold;
        height: auto;
    }
    .error {
        color: $error;
        text-style: bold;
        height: auto;
    }
    .warn {
        color: $warn;
        height: auto;
    }

    /* ── Boutons ─────────────────────────────────────────────────────── */
    Button {
        margin: 0 1;
        height: 3;
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
        height: 3;
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
        height: auto;
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
        margin: 0 0 1 0;
        height: auto;
    }
    .toolbar {
        height: 5;
        dock: bottom;
        background: $surface;
        border-top: solid $border;
        align: center middle;
        padding: 1 2;
    }
    .center {
        align: center middle;
        height: auto;
    }
    .row {
        layout: horizontal;
        height: auto;
    }

    /* ── Survey scroll ───────────────────────────────────────────────── */
    #survey_scroll {
        height: 1fr;
        padding: 0 1;
    }
    #survey_toolbar {
        height: 5;
        dock: bottom;
        background: $surface;
        border-top: solid $border;
        align: center middle;
        padding: 1 2;
    }

    /* ── Checkbox ────────────────────────────────────────────────────── */
    Checkbox {
        background: $bg;
        color: $text;
        height: auto;
        padding: 0 1;
        margin: 0;
    }
    Checkbox:focus {
        background: $surface;
    }
    Checkbox:hover {
        background: $surface;
    }

    /* ── RadioSet ────────────────────────────────────────────────────── */
    RadioSet {
        background: $bg;
        border: solid $border;
        padding: 0 1;
        height: auto;
    }
    RadioButton {
        color: $text;
        height: auto;
        padding: 0 1;
        margin: 0;
    }
    RadioButton:hover {
        background: $surface;
    }

    /* ── Select ──────────────────────────────────────────────────────── */
    Select {
        background: $surface;
        border: solid $border;
        height: auto;
    }

    /* ── ProgressBar ─────────────────────────────────────────────────── */
    ProgressBar {
        color: $accent;
        height: auto;
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
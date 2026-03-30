"""
IdeaForge — ui/screens/projects_list.py
Écran d'affichage de tous les projets générés.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Footer, Label, ListItem, ListView, Static
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual import on

from core.projects import load_projects
from core.logger import log


class ProjectsListScreen(Screen):
    """Affiche la liste de tous les projets générés."""

    def __init__(self) -> None:
        super().__init__()
        self._projects: list[dict] = []
        self._selected_idx: int | None = None

    # ── Composition ──────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        self._projects = load_projects()

        yield Static("📋  Projets générés", classes="title")
        yield Static(
            f"{len(self._projects)} projet(s) enregistré(s)",
            classes="subtitle",
        )

        with Horizontal():
            # Liste de noms
            with Vertical(id="pane_list"):
                if self._projects:
                    yield ListView(
                        *[
                            ListItem(Label(p.get("name", f"Projet {i+1}")), id=f"p_{i}")
                            for i, p in enumerate(self._projects)
                        ],
                        id="project_list",
                    )
                else:
                    yield Static(
                        "Aucun projet pour l'instant.\nGénérez votre première idée !",
                        classes="muted",
                    )

            # Détail du projet sélectionné
            with ScrollableContainer(id="pane_detail"):
                yield Static("Sélectionnez un projet dans la liste.", id="detail_content", classes="muted")

        with Horizontal(classes="toolbar"):
            yield Button("← Retour", id="btn_back")

        yield Footer()

    # ── Affichage du détail ───────────────────────────────────────────────────

    def _show_project(self, idx: int) -> None:
        if idx < 0 or idx >= len(self._projects):
            return
        p = self._projects[idx]

        detail = self.query_one("#pane_detail", ScrollableContainer)
        detail.remove_children()

        detail.mount(Static(p.get("name", "—"), classes="title"))

        blocks = [
            ("Description",             p.get("description", "—")),
            ("Langage / Technologie",   p.get("language", "—")),
            ("Détails",                 p.get("details", "—")),
        ]
        for label_text, value in blocks:
            v = Vertical(classes="card")
            v.mount(Label(label_text, classes="muted"))
            v.mount(Static(value))
            detail.mount(v)

    # ── Événements ───────────────────────────────────────────────────────────

    @on(ListView.Selected, "#project_list")
    def on_project_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id  # format : "p_<idx>"
        if item_id and item_id.startswith("p_"):
            try:
                idx = int(item_id[2:])
                self._selected_idx = idx
                self._show_project(idx)
            except ValueError:
                pass

    @on(Button.Pressed, "#btn_back")
    def action_back(self) -> None:
        self.app.pop_screen()

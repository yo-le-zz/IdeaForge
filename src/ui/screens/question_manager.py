"""
IdeaForge — ui/screens/question_manager.py
Écran de gestion CRUD des questions.
"""

from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Button, Checkbox, Footer, Input, Label,
    ListItem, ListView, RadioButton, RadioSet, Static,
)
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual import on

from core.questions import load_questions, add_question, delete_question, update_question
from core.logger import log


class QuestionManagerScreen(Screen):
    """Écran de gestion des questions."""

    def __init__(self, message: str = "") -> None:
        super().__init__()
        self._message = message
        self._questions: list[dict] = []
        self._selected_id: str | None = None

    # ── Composition ──────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        self._questions = load_questions()

        yield Static("⚙  Gestion des questions", classes="title")

        if self._message:
            yield Static(self._message, classes="warn")

        with Horizontal():
            # Panneau gauche : liste des questions
            with Vertical(id="panel_list"):
                yield Static("Questions existantes", classes="section-title")
                yield ListView(
                    *[
                        ListItem(Label(f"[{q['type']}] {q['texte'][:50]}"), id=f"q_{q['id']}")
                        for q in self._questions
                    ],
                    id="question_list",
                )
                with Horizontal(classes="row"):
                    yield Button("🗑 Supprimer", id="btn_delete", classes="danger")
                    yield Button("✏ Modifier", id="btn_edit")

            # Panneau droit : formulaire d'ajout/édition
            with ScrollableContainer(id="panel_form"):
                yield Static("Ajouter une question", classes="section-title", id="form_title")
                yield Label("Texte de la question *")
                yield Input(placeholder="Ex: Quel est ton langage préféré ?", id="inp_texte")
                yield Label("Type *")
                yield RadioSet(
                    RadioButton("Choix (liste d'options)", value=True, id="rb_choix"),
                    RadioButton("Texte libre", id="rb_texte"),
                    id="radio_type",
                )
                yield Label("Options (une par ligne, uniquement pour type Choix)", id="lbl_options")
                yield Input(placeholder="Python, JavaScript, Rust, …", id="inp_options")
                yield Checkbox("Choix multiples autorisés", id="chk_multi")
                yield Label("Longueur max (texte libre)", id="lbl_maxlen")
                yield Input(value="200", id="inp_maxlen")
                with Horizontal(classes="row"):
                    yield Button("➕ Ajouter", id="btn_add", classes="success")
                    yield Button("💾 Sauvegarder", id="btn_save", classes="primary")
                    yield Button("↩ Réinitialiser", id="btn_reset")

        with Horizontal(classes="toolbar"):
            yield Button("← Retour", id="btn_back")

        yield Footer()

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _refresh_list(self) -> None:
        """Recharge et met à jour la ListView."""
        self._questions = load_questions()
        lv = self.query_one("#question_list", ListView)
        lv.clear()
        for q in self._questions:
            lv.append(ListItem(Label(f"[{q['type']}] {q['texte'][:50]}"), id=f"q_{q['id']}"))

    def _get_form_values(self) -> dict:
        """Récupère les valeurs du formulaire."""
        texte   = self.query_one("#inp_texte", Input).value.strip()
        options_raw = self.query_one("#inp_options", Input).value.strip()
        options = [o.strip() for o in options_raw.split(",") if o.strip()]
        multi   = self.query_one("#chk_multi", Checkbox).value
        maxlen_raw = self.query_one("#inp_maxlen", Input).value.strip()
        try:
            maxlen = int(maxlen_raw)
        except ValueError:
            maxlen = 200

        # Détermine le type sélectionné via RadioSet
        radio = self.query_one("#radio_type", RadioSet)
        type_ = "choix" if radio.pressed_index == 0 else "texte"

        return {
            "texte": texte,
            "type_": type_,
            "options": options,
            "multi": multi,
            "max_length": maxlen,
        }

    def _clear_form(self) -> None:
        """Remet le formulaire à zéro."""
        self.query_one("#inp_texte", Input).value = ""
        self.query_one("#inp_options", Input).value = ""
        self.query_one("#chk_multi", Checkbox).value = False
        self.query_one("#inp_maxlen", Input).value = "200"
        self.query_one("#form_title", Static).update("Ajouter une question")
        self._selected_id = None

    def _set_form_from_question(self, q: dict) -> None:
        """Pré-remplit le formulaire à partir d'une question existante."""
        self.query_one("#inp_texte", Input).value  = q.get("texte", "")
        self.query_one("#chk_multi", Checkbox).value = q.get("multi", False)
        self.query_one("#inp_maxlen", Input).value   = str(q.get("max_length", 200))
        options = q.get("options", [])
        self.query_one("#inp_options", Input).value  = ", ".join(options)
        self.query_one("#form_title", Static).update(f"Modifier : {q['texte'][:30]}")
        self._selected_id = q["id"]

    # ── Événements ───────────────────────────────────────────────────────────

    @on(Button.Pressed, "#btn_back")
    def action_back(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, "#btn_reset")
    def action_reset(self) -> None:
        self._clear_form()

    @on(Button.Pressed, "#btn_add")
    def action_add(self) -> None:
        """Ajoute une nouvelle question."""
        vals = self._get_form_values()
        if not vals["texte"]:
            self.notify("Le texte de la question est obligatoire.", severity="error")
            return
        if vals["type_"] == "choix" and not vals["options"]:
            self.notify("Ajoutez au moins une option pour un type 'choix'.", severity="warning")
            return
        try:
            add_question(**vals)
            self._refresh_list()
            self._clear_form()
            self.notify("Question ajoutée ✓", severity="information")
        except Exception as exc:
            log.error("Erreur ajout question : %s", exc)
            self.notify(str(exc), severity="error")

    @on(Button.Pressed, "#btn_save")
    def action_save(self) -> None:
        """Modifie une question existante."""
        if not self._selected_id:
            self.notify("Sélectionnez d'abord une question à modifier.", severity="warning")
            return
        vals = self._get_form_values()
        if not vals["texte"]:
            self.notify("Le texte est obligatoire.", severity="error")
            return
        try:
            update_question(
                self._selected_id,
                texte=vals["texte"],
                type=vals["type_"],
                options=vals["options"],
                multi=vals["multi"],
                max_length=vals["max_length"],
            )
            self._refresh_list()
            self._clear_form()
            self.notify("Question modifiée ✓", severity="information")
        except Exception as exc:
            log.error("Erreur modification : %s", exc)
            self.notify(str(exc), severity="error")

    @on(Button.Pressed, "#btn_delete")
    def action_delete(self) -> None:
        """Supprime la question sélectionnée."""
        if not self._selected_id:
            self.notify("Sélectionnez d'abord une question.", severity="warning")
            return
        delete_question(self._selected_id)
        self._refresh_list()
        self._clear_form()
        self.notify("Question supprimée.", severity="information")

    @on(Button.Pressed, "#btn_edit")
    def action_edit(self) -> None:
        """Pré-remplit le formulaire avec la question sélectionnée."""
        if not self._selected_id:
            self.notify("Sélectionnez d'abord une question.", severity="warning")
            return
        for q in self._questions:
            if q["id"] == self._selected_id:
                self._set_form_from_question(q)
                return

    @on(ListView.Selected, "#question_list")
    def on_list_selected(self, event: ListView.Selected) -> None:
        """Mémorise l'ID de la question cliquée dans la liste."""
        item_id = event.item.id  # format : "q_<uuid>"
        if item_id and item_id.startswith("q_"):
            self._selected_id = item_id[2:]

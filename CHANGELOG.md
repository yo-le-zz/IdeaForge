# Changelog — IdeaForge

Toutes les modifications notables de ce projet sont documentées ici.
Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

---

## [V1.0.0] — 2025

### Corrigé
- `survey.py` — crash au lancement du formulaire (`MountError: Can't mount <class 'generator'>`) causé par l'usage de `with container: yield` dans `_build_question_widget`. Remplacé par une construction via liste `children` passée au constructeur `Vertical(*children)`
- `survey.py` — normalisation des IDs de checkboxes : le caractère `/` est maintenant remplacé dans `safe_opt` pour éviter des IDs invalides
- `welcome.py` — import de `ErrorScreen` via `__import__` remplacé par un import direct
- `generating.py` — le bouton Annuler ne faisait pas le bon nombre de `pop_screen()`. Réduit à un seul appel cohérent avec la pile
- `generating.py` — `_on_success` utilise désormais `switch_screen` au lieu d'empiler un écran supplémentaire
- `result.py` — bouton "Accueil" effectue deux `pop_screen()` successifs pour vider proprement la pile (result → survey → welcome)
- `result.py` — bouton "Générer une autre idée" pop d'abord le result puis switch le survey pour éviter une pile infinie

---

## [V1.0.0] — 2025

### Ajouté
- Interface terminal interactive avec **Textual**
- Gestion CRUD complète des questions (ajout / modification / suppression)
- Types de questions : `choix` (radio ou checkbox) et `texte libre`
- Formulaire de réponse dynamique généré depuis `questions.json`
- Intégration **Ollama** via API HTTP locale (modèle configurable)
- Génération d'idées de projets en JSON structuré (`name`, `description`, `language`, `details`)
- Détection et évitement automatique des doublons
- Persistance des projets dans `data/projects.json`
- Boucle infinie de génération sans répétition
- Logs détaillés dans `ideaforge.log`
- Gestion des erreurs : JSON corrompu, Ollama hors ligne, timeout
- Argument `--version` en ligne de commande
- Script de compilation **Nuitka** (`build.py`)
- Variable de version unique (`APP_VERSION` / `APP_VERSION_FULL`) propagée dans tout le projet
- 5 questions exemples incluses dans `data/questions.json`
- Compatible **Windows 11**

---

_IdeaForge — Créé par yo-le-zz_
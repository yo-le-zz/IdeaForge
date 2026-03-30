# Changelog — IdeaForge

Toutes les modifications notables de ce projet sont documentées ici.
Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

---

## [V1.0.0] — 2024

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

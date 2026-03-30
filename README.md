# IdeaForge V1.0.0

> Générateur d'idées de projets informatiques via IA locale (Ollama) — Interface terminal interactive (Textual)

**Créateur : yo-le-zz**

---

## ✨ Présentation

IdeaForge est un outil CLI interactif qui vous aide à trouver votre prochain projet de programmation. Il vous pose une série de questions personnalisables, envoie vos réponses à un modèle IA local via **Ollama**, et génère une idée de projet unique — sans jamais répéter deux fois la même idée.

---

## 📂 Structure du projet

```
IdeaForge/
├── src/
│   ├── main.py              ← Point d'entrée
│   ├── core/
│   │   ├── config.py        ← Configuration centralisée
│   │   ├── logger.py        ← Logs (fichier + console)
│   │   ├── questions.py     ← Gestion CRUD des questions
│   │   ├── projects.py      ← Stockage & déduplication
│   │   └── ollama_client.py ← Intégration Ollama
│   └── ui/
│       ├── app.py           ← App Textual principale
│       └── screens/
│           ├── welcome.py
│           ├── question_manager.py
│           ├── survey.py
│           ├── generating.py
│           ├── result.py
│           ├── projects_list.py
│           └── error_screen.py
├── data/
│   ├── questions.json       ← Questions (éditables)
│   └── projects.json        ← Projets générés (historique)
├── assets/
│   └── icon.ico
├── dist/                    ← Sortie de compilation Nuitka
├── requirements.txt
├── LICENSE
├── README.md
└── CHANGELOG.md
```

---

## 🚀 Installation & Lancement

### Prérequis

- Python 3.10+
- [Ollama](https://ollama.com/) installé et lancé localement
- Un modèle téléchargé (ex: `mistral`)

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Démarrer Ollama

```bash
ollama serve
ollama pull mistral
```

### 3. Lancer IdeaForge

```bash
python src/main.py
```

### Afficher la version

```bash
python src/main.py --version
# → 1.0.0
```

---

## ⚙️ Configuration

Éditez `src/core/config.py` pour personnaliser :

| Variable          | Défaut                              | Description                        |
|-------------------|-------------------------------------|------------------------------------|
| `OLLAMA_MODEL`    | `"mistral"`                         | Modèle Ollama utilisé              |
| `OLLAMA_API_URL`  | `http://localhost:11434/api/generate` | URL de l'API Ollama              |
| `OLLAMA_TIMEOUT`  | `120`                               | Timeout en secondes                |
| `MAX_RETRIES_DUPLICATE` | `5`                          | Tentatives max si doublon          |

---

## 📝 Gestion des questions

Les questions sont stockées dans `data/questions.json`. Vous pouvez :
- Les éditer directement dans le fichier JSON
- Utiliser l'interface intégrée (**⚙ Gérer les questions**)

### Format d'une question

```json
{
  "id": "identifiant_unique",
  "texte": "Votre question ?",
  "type": "choix",
  "options": ["Option A", "Option B"],
  "multi": false
}
```

```json
{
  "id": "identifiant_unique",
  "texte": "Décrivez votre contrainte",
  "type": "texte",
  "max_length": 300
}
```

---

## 🔨 Compilation Nuitka (Windows)

```bash
python build.py
```

Le `.exe` est généré dans `dist/`.

---

## 📄 Licence

Voir [LICENSE](LICENSE) — Usage libre avec attribution obligatoire à **yo-le-zz / IdeaForge**.

---

## 🤝 Crédits

- **Créateur** : yo-le-zz
- **UI** : [Textual](https://github.com/Textualize/textual) by Textualize
- **IA locale** : [Ollama](https://ollama.com/)

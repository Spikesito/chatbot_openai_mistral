# SEGURET Emile - FERNANDES Adrien - DANY Raphael  
**M1 Data Science — Module NLP**

## Introduction

Ce projet a été réalisé dans le cadre du module de NLP en M1 Data Science.  
Il s'agit d'un projet de chatbot spécialisé sur le jeu Brawl Stars, permettant d’interagir avec une base de données **ChromaDB** et d’alimenter un backend de type RAG (Retrieval-Augmented Generation).
Le projet inclut également une interface utilisateur développée avec **Streamlit**, permettant de :

- Télécharger des fichiers pour enrichir la base,
- Interagir avec le chatbot en texte ou en audio(si vous recréez le projet),
- Analyser des images
- Visualiser les résultats de l'API.

> ⚠️ À noter : le projet est également **dockerisé** pour un déploiement facilité. Deux modes de lancement sont donc possibles. Aussi nous avons hébergé un exemple du projet sur le lien : http://emileseguret.synology.me:9090/ (l'audio marche uniquement si vous lancez vous même le projet mais l'url http empêche l'audio)

---

## Structure du projet

- `.streamlit/secrets.toml` : Fichier de configuration contenant les clés API (à créer, voir section *Installation*).
- `chromadb/` : Dossier contenant les données de la base ChromaDB.
- `datascience/` : Notebooks Jupyter réalisés durant les TPs.
- `downloaded_files/` : Fichiers envoyés via l’interface :
  - `images/` : Fichiers images déposés par l'utilisateur pour analyse. 
  - `raw/` : Fichiers originaux (PDF, etc.),
  - `prepared/` : Fichiers traités et insérés dans la base.
- `pages/` : Pages supplémentaires de l'application Streamlit.
- `utils/` : Fonctions principales utilisées par le frontend.
- `Multimodel-Bot.py` : Application principale Streamlit.
- `requirements.txt` : Fichier listant les dépendances Python.
- `Dockerfile` : Fichier décrivant comment construire l'image Docker de l'application.
- `docker-compose.yml` : Fichier permettant de lancer facilement l'application avec ses services (API, interface Streamlit, base de données, etc.) via Docker Compose.

---

## Installation

1. **Création du fichier de secrets** :  
Créez un dossier `.streamlit` à la racine du projet avec un fichier `secrets.toml` contenant vos clés API :

```toml
MISTRAL_API_KEY = "<votre clé API Mistral>"
OPENAI_API_KEY = "<votre clé API OpenAI>"
```

2. **Création de l’environnement virtuel** :  
```bash
python -m venv .venv/mon_env
```

> 🛑 Attention : Le fichier `.gitignore` ignore les dossiers `.venv/`. Pensez à bien nommer votre environnement avec ce préfixe si vous faites fork et un `git push`.

3. **Activation de l’environnement virtuel** (Windows) :
```bash
.venv/mon_env/Scripts/activate
```

4. **Installation des dépendances** :
```bash
pip install -r requirements.txt
```


## Lancement du projet

1. **Création du fichier de secrets** :  
Créez un dossier `.streamlit` à la racine du projet avec un fichier `secrets.toml` contenant vos clés API :

```toml
# Retirer le point au milieu du mot KEY :
MISTRAL_API_KE.Y = "<votre clé API Mistral>"
OPENAI_API_KE.Y = "<votre clé API OpenAI>"
```

### ➤ Option 1 : Lancement manuel (en local)

1. **Création de l’environnement virtuel** :  
```bash
python -m venv .venv/mon_env
```

> 🛑 Attention : Le fichier `.gitignore` ignore les dossiers `.venv/`. Pensez à bien nommer votre environnement avec ce préfixe si vous faites fork et un `git push`.

2. **Activation de l’environnement virtuel** (Windows) :
```bash
.venv/mon_env/Scripts/activate
```

3. **Installation des dépendances** :
```bash
pip install -r requirements.txt
```

Depuis la racine du projet :

```bash
streamlit run Multimodal-Bot.py
```

### ➤ Option 2 : Lancement avec Docker

Assurez-vous d’avoir **Docker** installé, puis à la racine du projet :

```bash
docker compose up --build
```

L’interface sera accessible sur : [http://localhost:8501](http://localhost:8501)

## Remarques

- L'audio n'est pas fonctionnel sur l'url [http://emileseguret.synology.me:9090/](http://emileseguret.synology.me:9090/) mais marche bien si vous lancez le projet vous même.
- La fonctionnalité audio requiert un micro fonctionnel.
- La base ChromaDB a en historique les fichiers déjà déposés mais vous pouvez la réintialiser et ajouter des documents dans la page **RAG-Manager.py**.

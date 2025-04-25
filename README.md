# SEGURET Emile - FERNANDES Adrien - DANY Raphael M1 Data Science

## Introduction

Ce projet a été réalisé dans le cadre du module de machine learning en M1 Data Science. Il s'agit d'une API développée avec la bibliothèque FASTAPI, permettant d'intéragir avec notre base de donnée ChromaDB et notre backend. Le projet inclut également une application Streamlit pour le frontend pour interagir avec l'API et télécharger des fichiers pour le RAG, discuter avec le chatbot que ce soit par écrit ou via la fonctionnalité audio.

## Structure du projet

Le projet est structuré en plusieurs fichiers :

- `.streamlit/secrets.toml` : Le fichier `secrets.toml` dans le dossier `.streamlit/` sont à créer à l'init du projet (cf. Section Installation).
- `chromadb/` : Le dossier contenant la base de donnée ChromaDB.
- `datascience/` : Le dossier contenant nos notebooks des TPs réalisés en cours.
- `downloaded_files/` : Le dossier contenant les fichiers déposés via le front `raw/` pour les fichiers pdf et `prepared/` pour ceux traités et insérés dans la db.
- `functions/` : Le dossier contenant les fonctions principales.
- `pages/` : Le dossier contenant nos différentes pages.
- `api.py` : Le fichier principal contenant l'API développée avec FASTAPI.
- `Chatbot-RAG.py` : L'application front développée avec Streamlit pour interagir avec l'API + le dossier `pages` pour nos différentes pages.
- `requirements.txt` : Les dépendances nécessaires au projet.

## Installation

Pour installer les dépendances nécessaires, exécutez la commande suivante dans un terminal :

Créer un dossier `.streamlit/` à la racine du projet contenant un fichier à créer `secrets.toml`.
Ajouter ces lignes dans le fichier nouvellement créé : 
```shell
MISTRAL_API_KEY = "<votre clé API mistral>"
OPENAI_API_KEY = "<votre clé API openai>"
```

Ensuite placez vous à la racine de votre projet et créez un environnement virtuel pour votre projet : 
```shell
python -m venv .venv\nom_de_votre_environnement
```
Attention le fichier `.gitignore` est configuré pour ignorer le dossier `.venv\` donc nommez votre environnement virtuel en commençant par `.venv\` afin qu'il ne soit pas pris en compte dans un push du projet si vous faites un fork.

Activez votre environnement virtuel : 
```shell
.venv\nom_de_votre_environnement\Scripts\activate
```

Enfin une fois votre environnement virtuel activé lancez cette commande pour installer toutes les librairies du projet :
```shell
pip install -r requirements.txt
```

## Lancement à la racine du dossier

L'application streamlit :
```shell
streamlit run .\Chatbot-RAG.py
```

L'API :
```shell
uvicorn api:app --reload
```

## Vidéo démonstration

[![Démonstration](https://img.youtube.com/vi/6tOiAZUkzM0/0.jpg)](https://youtu.be/6tOiAZUkzM0)
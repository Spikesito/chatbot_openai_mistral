# Caetano Jean-Philippe - Seguret Emile - Dechavanne Lucas B3/IA DATA

## Introduction

Ce projet a été réalisé dans le cadre du module de machine learning en M1 Data Science. Il s'agit d'une API développée avec la bibliothèque FASTAPI, permettant d'entraîner un modèle sur un jeu de données fourni et de réaliser des prédictions à partir du modèle entraîné. Le projet inclut également une application Streamlit pour interagir avec l'API et télécharger le modèle entraîné.

## Structure du projet

Le projet est structuré en plusieurs fichiers :

- `api.py` : Le fichier principal contenant l'API développée avec FASTAPI.
- `requirements.txt` : Les dépendances nécessaires au projet.
- `function` : Le dossier contenant les fonctions principales.
- `app.py` : L'application front développée avec Streamlit pour interagir avec l'API + le dossier `pages` pour nos différentes pages.
- `model` : Le fichier contenant le modèle entraîné utilisé pour les prédictions.
- `marketing_campaign.csv` : Le jeu de données utilisé pour l'entraînement.
- `Datascience` : Le dossier de notebooks contenant l’analyse exploratoire et la conception du modèles. Il y'a nos trois fichier d'exploration et le fichier `DataScience` final.

## Installation

Pour installer les dépendances nécessaires, exécutez la commande suivante :

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
```bash
streamlit run .\app.py
```

L'API :
```bash
uvicorn api:app --reload
```

## Vidéo démonstration

[![Démonstration](https://img.youtube.com/vi/6tOiAZUkzM0/0.jpg)](https://youtu.be/6tOiAZUkzM0)
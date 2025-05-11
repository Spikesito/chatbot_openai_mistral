# Utilise une image Python officielle
FROM python:3.11-slim

# Dossier de travail
WORKDIR /app

# Copier tous les fichiers dans l'image
COPY . .

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Lancer ton app principale
CMD ["streamlit", "run", "Multimodal-Bot.py", "--server.port=8501", "--server.address=0.0.0.0"]
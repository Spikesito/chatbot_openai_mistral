# Utilise une image Python officielle
FROM python:3.11-slim

# Variables d'environnement Streamlit
ENV STREAMLIT_SERVER_HEADLESS true
ENV STREAMLIT_SERVER_PORT 8501
ENV STREAMLIT_SERVER_ENABLECORS false
ENV STREAMLIT_SERVER_ENABLEXSRFPROTECTION false

# Dossier de travail
WORKDIR /app

# Copier tous les fichiers dans l'image
COPY . .

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Lancer ton app principale
CMD ["streamlit", "run", "Multimodal-Bot.py"]
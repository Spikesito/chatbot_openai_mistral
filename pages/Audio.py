import streamlit as st
from openai import OpenAI

# ---------------- Connexion à OpenAI ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

audio_value = st.audio_input("Record a voice message")

if audio_value is not None:
    st.audio(audio_value)

    # Transcription audio
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_value,  
        response_format="text"
    )

    # Affichage de la transcription
    st.write(transcription.text)

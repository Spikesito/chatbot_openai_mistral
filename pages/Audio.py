import streamlit as st
from openai import OpenAI

# ---------------- Connexion à OpenAI ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

audio_value = st.audio_input("Record a voice message")

if audio_value is not None:
    # Transcription audio
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_value,  
    )
    st.write(transcription.text)

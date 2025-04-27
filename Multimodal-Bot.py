import io
import streamlit as st
from utils.openai_utils import generate_image, chat_with_openai, chat_with_rag_context, transcribe_audio
from utils.chromadb_utils import list_collections, query_collection

st.title("Chatbot Multimodal")

# ---------------- INIT ----------------
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages_multimodal" not in st.session_state:
    st.session_state.messages_multimodal = []
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

# ---------------- SIDEBAR ---------------
st.sidebar.subheader("RAG : Recherche Augmentée")
use_rag = st.sidebar.checkbox("Activer le mode RAG", value=False)

st.sidebar.subheader("Choix de la base de connaissances :")
collections = list_collections()
collection_name = st.sidebar.selectbox("Collection active", ["Aucune"] + collections)

st.sidebar.markdown("---")

st.sidebar.subheader("Prompt Audio :")
audio_value = st.sidebar.audio_input("Appuyez pour enregistrer votre question :")

if use_rag and (not collection_name or collection_name == "Aucune"):
    st.warning("🔎 RAG activé, mais aucune collection sélectionnée.")

# ---------------- HANDLE PROMPT ----------------
def handle_prompt(prompt):
    if prompt == "clear":
        st.session_state.messages_multimodal = []
        st.rerun()
    elif prompt.startswith("/image"):
        img_prompt = prompt.replace("/image", "").strip()
        if img_prompt : 
            with st.spinner("📝 Transcription en cours..."):
                try:
                    return {"type": "image", "url": generate_image(img_prompt)}
                except ValueError as ve:
                    return str(ve)
        return "Merci d'ajouter une description."
    elif use_rag:
        if collection_name and collection_name != "Aucune":
            docs = query_collection(collection_name, prompt)
            return chat_with_rag_context(prompt, str(docs), model=st.session_state["openai_model"])
        else:
            return "Merci de sélectionner une collection pour utiliser le mode RAG."
    else:
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages_multimodal
            if isinstance(m["content"], str) and m["content"].strip() != ""
        ]
        messages.append({"role": "user", "content": prompt})
        return chat_with_openai(messages, st.session_state["openai_model"])

# ---------------- INPUT TEXTE ----------------
if prompt := st.chat_input("Message ou commande /image une voiture volante"):
    st.session_state.messages_multimodal.append({"role": "user", "content": prompt})
    result = handle_prompt(prompt)
    st.session_state.messages_multimodal.append({"role": "assistant", "content": result})

# ---------------- INPUT AUDIO ----------------
if audio_value:
    st.session_state.audio_bytes = audio_value.getvalue()

if st.session_state.audio_bytes:
    if st.sidebar.button("Envoyer l'audio"):
        audio_file = io.BytesIO(st.session_state.audio_bytes)
        audio_file.name = "voice_input.mp3"

        with st.spinner("📝 Transcription en cours..."):
            transcript = transcribe_audio(audio_file)

        st.session_state.messages_multimodal.append({"role": "user", "content": transcript})
        result = handle_prompt(transcript)
        st.session_state.messages_multimodal.append({"role": "assistant", "content": result})

        # Nettoyage
        audio_file.close()
        st.session_state.audio_bytes = None

# ---------------- AFFICHAGE HISTORIQUE CHAT ----------------
for message in st.session_state.messages_multimodal:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], dict) and message["content"].get("type") == "image":
            st.image(message["content"]["url"])
        else:
            st.markdown(message["content"])

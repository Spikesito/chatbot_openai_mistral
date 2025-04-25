import streamlit as st
import os
import shutil
from openai import OpenAI

st.title("🧠 Chatbot Multimodal")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialisation
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and isinstance(message["content"], dict) and message["content"].get("type") == "image":
            st.image(message["content"]["url"])
        else:
            st.markdown(message["content"])

# Fonction principale
def handle_prompt(prompt):
    # Nettoyage
    if prompt == "clear":
        st.session_state.messages = []
        st.rerun()

    # Génération d’image via /image [prompt]
    elif prompt.startswith("/image"):
        image_prompt = prompt.replace("/image", "").strip()
        if not image_prompt:
            return "❗ Merci d'ajouter une description après `/image`"

        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return {"type": "image", "url": image_url}

    # Cas standard : discussion textuelle
    else:
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content

# Interface de chat
if prompt := st.chat_input("Tape ton message ou une commande comme /image une licorne dans l’espace"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        result = handle_prompt(prompt)
        if isinstance(result, dict) and result.get("type") == "image":
            st.image(result["url"])
        else:
            st.markdown(result)

    st.session_state.messages.append({"role": "assistant", "content": result})
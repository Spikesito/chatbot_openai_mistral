import streamlit as st
import os
import shutil
import base64
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
        if isinstance(message["content"], dict) and message["content"].get("type") == "image":
            st.image(message["content"]["url"])
        else:
            st.markdown(message["content"])

  # Fonction d'encodage l'image en base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")



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

#fontion d'analyse d'image
def analyse_image(image_path):
    # Téléchargement de l'image
    base64_image = encode_image(image_path)

    # Appel à l'API pour l'analyse d'image
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": "what's in this image?" },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )

    return response.output_text

# Exploration des fichiers
uploaded_image = st.file_uploader("Télécharge une image", type=["jpg", "jpeg", "png"], key="file_uploader")

if uploaded_image:

    path = f"./downloaded_files/images/{uploaded_image.name}"
    with open(path, 'wb') as f:
        f.write(uploaded_image.getbuffer())

    result = analyse_image(path)
    st.session_state.messages.append({"role": "user", "content": {"type": "image", "url":path}})

    st.session_state.messages.append({"role": "assistant", "content": result})

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
import streamlit as st
import os
import io
import shutil
from openai import OpenAI
import chromadb
from pydub import AudioSegment

# ---------------- Initialisation ------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
chroma_client = chromadb.PersistentClient(path="./chromadb")

# ---------------- Sidebar : Choix collection ------------------
st.sidebar.subheader("📂 Choix de la collection")
list_collections = [col.name for col in chroma_client.list_collections()]
collection_name = st.sidebar.selectbox("Sélectionnez la base à utiliser comme contexte", list_collections)

# ---------------- Sidebar : Customisation ------------------
st.sidebar.subheader("🔧 Personnalisation du RAG")
collection_name = st.sidebar.selectbox("Sélectionnez la collection", list_collections + ["New Collection"])
if collection_name == 'New Collection':
    collection_name = st.sidebar.text_input("Nom de la nouvelle collection")

uploaded_file = st.sidebar.file_uploader("Téléchargez un fichier PDF", type="pdf", label_visibility="collapsed")

if uploaded_file:
    uploaded_file_name = uploaded_file.name.replace(".pdf", "")
    with open(f"./downloaded_files/raw/{uploaded_file_name}.pdf", 'wb') as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Traitement du fichier", show_time=True):
        os.system(f"marker_single ./downloaded_files/raw/{uploaded_file.name} --output_dir ./downloaded_files/prepared/")

    with open(f"./downloaded_files/prepared/{uploaded_file_name}/{uploaded_file_name}.md", 'r') as f:
        data = f.read()

    chunks = data.split("# ")[1:]
    collection = chroma_client.get_or_create_collection(collection_name.replace(" ", "_"))
    collection.add(ids=[str(i) for i in range(len(chunks))], documents=chunks)

    collection.query(query_texts=["What is the best brawler?"], n_results=2)
    st.sidebar.success("Fichier téléchargé et converti avec succès !")

# ---------------- Sidebar : Fichiers téléchargés ------------------
UPLOAD_FOLDER = "./downloaded_files/raw/"
IGNORED_FILES = [".gitignore"]

st.sidebar.subheader("📂 Fichiers présents")
files = [f for f in os.listdir(UPLOAD_FOLDER) if f not in IGNORED_FILES]

for file in files:
    col1, col2 = st.sidebar.columns([4, 1])
    col1.write(file)
    if col2.button("🗑️", key=f"del_{file}"):
        path = os.path.join(UPLOAD_FOLDER, file)
        folder = os.path.splitext(file)[0]
        shutil.rmtree(os.path.join(UPLOAD_FOLDER, folder), ignore_errors=True)
        os.remove(path)

# ---------------- CHATBOT RAG ------------------
st.title("Chatbot RAG")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def get_response_from_gpt_with_rag(prompt, collection_name):
    collection = chroma_client.get_collection(name=collection_name)
    docs = str(collection.query(query_texts=prompt, n_results=2, include=['documents'])["documents"])

    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {
                "role": 'system',
                "content": f"Tu es un assistant qui répond à l'utilisateur en te basant sur ce contexte : {docs}"
            },
            {
                "role": 'user',
                "content": prompt
            },
        ]
    )

    return response.choices[0].message.content


# ---------------- Fonction audio input + transcription + TTS ------------------
st.subheader("Parlez au micro")

audio_value = st.audio_input("Appuyez pour enregistrer une question vocale")

if audio_value:
    st.audio(audio_value)

    audio_bytes = audio_value.getvalue()
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "voice_input.mp3"

    with st.spinner("⏳ Transcription..."):
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    st.success("Transcription :")
    st.write(transcript)

    st.session_state.messages.append({"role": "user", "content": transcript})
    with st.chat_message("user"):
        st.markdown(transcript)

    response = get_response_from_gpt_with_rag(transcript, collection_name)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# ---------------- Texte manuel ------------------
if prompt := st.chat_input("Écrivez une question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = get_response_from_gpt_with_rag(prompt, collection_name)
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)

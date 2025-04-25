import streamlit as st
import os
import shutil
import base64
from openai import OpenAI
import chromadb

# ---------------- Connexions ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
chroma_client = chromadb.PersistentClient(path="./chromadb")

# ---------------- Sidebar ----------------
st.sidebar.title("🔧 Paramètres")

# ----- Sélection de la collection RAG -----
st.sidebar.subheader("📂 Choix de la collection")
collections = [col.name for col in chroma_client.list_collections()]
collection_name = st.sidebar.selectbox("Sélectionnez la collection", collections + ["New Collection"])

if collection_name == "New Collection":
    collection_name = st.sidebar.text_input("Nom de la nouvelle collection").replace(" ", "_")

# ----- Upload de PDF -----
st.sidebar.subheader("📄 Upload de document")
uploaded_file = st.sidebar.file_uploader("Téléchargez un fichier PDF", type="pdf")

if uploaded_file:
    file_name = uploaded_file.name.replace(".pdf", "")
    raw_path = f"./downloaded_files/raw/{file_name}.pdf"
    prepared_path = f"./downloaded_files/prepared/{file_name}/{file_name}.md"

    with open(raw_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("📚 Traitement du fichier..."):
        os.system(f"marker_single {raw_path} --output_dir ./downloaded_files/prepared/")

    with open(prepared_path, 'r') as f:
        data = f.read()

    chunks = data.split("# ")[1:]
    collection = chroma_client.get_or_create_collection(collection_name)
    collection.add(ids=[str(i) for i in range(len(chunks))], documents=chunks)

    st.sidebar.success("✅ Fichier converti et indexé avec succès !")

# ----- Upload d'image -----
st.sidebar.subheader("🖼️ Image à analyser")
uploaded_image = st.sidebar.file_uploader("Téléchargez une image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    with open("./downloaded_files/image.jpg", "wb") as f:
        f.write(uploaded_image.getbuffer())
    st.sidebar.success("✅ Image enregistrée ! Tapez /image dans le chat pour l’analyser.")

# ----- Fichiers visibles -----
st.sidebar.subheader("📁 Fichiers présents")
UPLOAD_FOLDER = "./downloaded_files/raw/"
IGNORED_FILES = [".gitignore"]
files = [f for f in os.listdir(UPLOAD_FOLDER) if f not in IGNORED_FILES]

for file in files:
    col1, col2 = st.sidebar.columns([4, 1])
    col1.write(file)
    if col2.button("🗑️", key=f"del_{file}"):
        path = os.path.join(UPLOAD_FOLDER, file)
        folder = os.path.splitext(file)[0]
        shutil.rmtree(os.path.join("./downloaded_files/prepared/", folder), ignore_errors=True)
        os.remove(path)

# ---------------- Fonctions ----------------
def get_response_from_gpt_with_rag(prompt, collection_name):
    collection = chroma_client.get_collection(name=collection_name)
    results = collection.query(query_texts=[prompt], n_results=2, include=['documents'])
    docs = str(results["documents"])

    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": f"Tu es un assistant qui répond avec ce contexte : {docs}"},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content

def analyse_uploaded_image():
    try:
        with open("./downloaded_files/image.jpg", "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        image_url = f"data:image/jpeg;base64,{image_base64}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "Décris cette image."},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ]},
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except FileNotFoundError:
        return " Aucune image disponible. Veuillez en uploader une dans la barre latérale."

# ---------------- Chatbot ----------------
st.title("Chatbot RAG + Analyse d'image")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur
if prompt := st.chat_input("Posez une question ou tapez /image pour analyser une image"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if prompt.strip().lower() == "/image":
            with st.spinner("🧐 Analyse de l’image en cours..."):
                response = analyse_uploaded_image()
        else:
            response = get_response_from_gpt_with_rag(prompt, collection_name)

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st
import os
from openai import OpenAI
import chromadb
import shutil

# ---------------Définition des connexions-----------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
chroma_client = chromadb.PersistentClient(path="./chromadb")


# ---------------Choix de la collection à utiliser---------------
st.sidebar.subheader("📂 Choix de la collection")
list_collections = [col.name for col in chroma_client.list_collections()]
collection_name = st.sidebar.selectbox("Sélectionnez la base à utiliser comme contexte", list_collections)


# ---------------Customation du RAG------------------------------
st.sidebar.subheader("🔧 Personnalisation du RAG")
# Possibilité de choisir une collection existante ou d'en créer une nouvelle
collection_name = st.sidebar.selectbox("Sélectionnez la collection", [col.name for col in chroma_client.list_collections()] + ["New Collection"])
if collection_name == 'New Collection':
    collection_name = st.sidebar.text_input("Nom de la nouvelle collection")

# Dépot du fichier à faire en RAG
uploaded_file = st.sidebar.file_uploader("Téléchargez un fichier PDF", type="pdf", label_visibility="collapsed")

# Traitement du fichier PDF
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
        collection.add(
            ids=[str(i) for i in range(len(chunks))],
            documents=chunks
        )

        collection.query(
            query_texts=["What is the best brawler?"],
            n_results=2
        )

        st.sidebar.success("Fichier téléchargé et converti avec succès !")

# Visibilité des fichiers téléchargés
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

# ---------------CHATBOT------------------------------
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

    docs = str(collection.query(
        query_texts=prompt,
        n_results=2,
        include = ['documents', 'distances']
    )["documents"])

    response = client.responses.create(
        model=st.session_state["openai_model"],
        input=[
            {
                "role":'system',
                "content":f"""Tu es un assistant polyvalent qui répond aux questions de ton utilisateur en te basant sur le contexte fourni.
                Voici la documentation dont tu disposes : {docs}
                """
            },
            {
                "role":'user',
                "content":prompt
            },
        ]
    )

    return response.output[0].content[0].text

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = get_response_from_gpt_with_rag(prompt, collection_name)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
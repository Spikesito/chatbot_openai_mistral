import streamlit as st
import os
import shutil

from services.chromadb_utils import (
    list_collections,
    add_documents_to_collection,
    delete_collection
)
from services.pdf_utils import save_uploaded_pdf, convert_pdf_to_chunks

# --------------- TITRE -----------------
st.title("📂 Gestion des collections & fichiers PDF")

# --------------- AJOUT D'UN PDF -----------------
st.subheader("➕ Ajouter un fichier PDF à une collection")

collection_name = st.selectbox("Collection", list_collections() + ["New Collection"])
if collection_name == "New Collection":
    collection_name = st.text_input("Nom de la nouvelle collection")

uploaded_file = st.file_uploader("📄 Déposer un PDF", type="pdf")
if uploaded_file and collection_name:
    filename = save_uploaded_pdf(uploaded_file)
    with st.spinner("⏳ Traitement du PDF..."):
        chunks = convert_pdf_to_chunks(filename)
        add_documents_to_collection(collection_name, chunks)
    st.success(f"✅ PDF '{uploaded_file.name}' ajouté à la collection '{collection_name}'")

# --------------- AFFICHAGE COLLECTIONS -----------------
st.subheader("🧠 Collections ChromaDB")

collections = list_collections()

if not collections:
    st.info("Aucune collection disponible.")
else:
    for collection in collections:
        col1, col2 = st.columns([4, 1])
        col1.write(collection)
        if col2.button("🗑️", key=f"delete_{collection}"):
            delete_collection(collection)
            st.success(f"✅ Collection '{collection}' supprimée.")
            st.rerun()

# --------------- AFFICHAGE FICHIERS -----------------
st.subheader("📁 Fichiers PDF téléchargés")

UPLOAD_FOLDER = "./downloaded_files/raw/"
IGNORED_FILES = [".gitignore"]

for file in os.listdir(UPLOAD_FOLDER):
    if file not in IGNORED_FILES:
        col1, col2 = st.columns([4, 1])
        col1.write(file)
        if col2.button("🗑️", key=f"del_{file}"):
            path = os.path.join(UPLOAD_FOLDER, file)
            folder = os.path.splitext(file)[0]
            shutil.rmtree(f"./downloaded_files/prepared/{folder}", ignore_errors=True)
            os.remove(path)
            st.success(f"🗑️ Fichier '{file}' supprimé.")
            st.rerun()

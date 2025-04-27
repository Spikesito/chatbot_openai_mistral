import streamlit as st
from services.openai_utils import generate_image, chat_with_openai

from services.chromadb_utils import list_collections, add_documents_to_collection, query_collection, delete_collection
from services.openai_utils import chat_with_rag_context
from services.pdf_utils import save_uploaded_pdf, convert_pdf_to_chunks

st.title("🧠 Chatbot Multimodal")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages_multimodal" not in st.session_state:
    st.session_state.messages_multimodal = []

for message in st.session_state.messages_multimodal:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], dict) and message["content"].get("type") == "image":
            st.image(message["content"]["url"])
        else:
            st.markdown(message["content"])

def handle_prompt(prompt):
    if prompt == "clear":
        st.session_state.messages_multimodal = []
        st.rerun()
    elif prompt.startswith("/image"):
        img_prompt = prompt.replace("/image", "").strip()
        if not img_prompt:
            return "❗ Merci d'ajouter une description."
        return {"type": "image", "url": generate_image(img_prompt)}
    elif use_rag:
        if collection_name and collection_name != "Aucune":
            docs = query_collection(collection_name, prompt)
            return chat_with_rag_context(prompt, str(docs), model=st.session_state["openai_model"])
        else:
            return "❗ Merci de sélectionner une collection pour utiliser le mode RAG."
    else:
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages_multimodal
            if isinstance(m["content"], str)
        ]
        messages.append({"role": "user", "content": prompt})
        return chat_with_openai(messages, st.session_state["openai_model"])
    
st.sidebar.subheader("📚 Collection ChromaDB")
collections = list_collections()
collection_name = st.sidebar.selectbox("Collection active", ["Aucune"] + collections)

st.sidebar.subheader("⚙️ RAG : Retrieval Augmented Generation")
use_rag = st.sidebar.checkbox("Activer le mode RAG", value=False)

if use_rag and (not collection_name or collection_name == "Aucune"):
    st.warning("🔎 RAG activé, mais aucune collection sélectionnée.")

if prompt := st.chat_input("Message ou commande /image une voiture volante"):
    st.session_state.messages_multimodal.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        result = handle_prompt(prompt)
        if isinstance(result, dict) and result.get("type") == "image":
            st.image(result["url"])
        else:
            st.markdown(result)

    st.session_state.messages_multimodal.append({"role": "assistant", "content": result})

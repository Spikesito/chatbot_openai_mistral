import streamlit as st
from utils.mistral_utils import chat_with_mistral_agent

st.title("🤖 Mistral Chatbot - Brawl Stars")

if "mistral_agent" not in st.session_state:
    st.session_state["mistral_agent"] = "ag:cf990a21:20250423:untitled-agent:88228b9f"
if "messages_mistral" not in st.session_state:
    st.session_state.messages_mistral = []

for message in st.session_state.messages_mistral:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pose ta question sur Brawl Stars..."):
    st.session_state.messages_mistral.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        result = chat_with_mistral_agent(
            agent_id=st.session_state["mistral_agent"],
            messages=st.session_state.messages_mistral,
            max_tokens=100
        )
        st.write(result)
        st.session_state.messages_mistral.append({"role": "assistant", "content": result})

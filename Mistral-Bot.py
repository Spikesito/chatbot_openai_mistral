from mistralai import Mistral
import streamlit as st

st.title("Mistral Chatbot for Brawl Stars")
st.write("This is a chatbot that can answer questions about Brawl Stars.")

# api_key = st.sidebar.text_input("Enter your Mistral API key", type="password")

client = Mistral(api_key=st.secrets["MISTRAL_API_KEY"])
# client = Mistral(api_key=api_key)

if "mistral_agent" not in st.session_state:
    st.session_state["mistral_agent"] = "ag:cf990a21:20250423:untitled-agent:88228b9f"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am a chatbot that can answer questions about Brawl Stars."},
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.agents.complete(
            agent_id=st.session_state["mistral_agent"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            max_tokens=100
        )
        result = stream.choices[0].message.content
        response = st.write(result)
    st.session_state.messages.append({"role": "assistant", "content": response})
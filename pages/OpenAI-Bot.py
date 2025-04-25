from openai import OpenAI
import streamlit as st

st.title("OpenAI Chatbot for Brawl Stars")
st.write("This is a chatbot that can answer questions about Brawl Stars.")

# api_key = st.sidebar.text_input("Enter your OPENAI API key", type="password")
# client = OpenAI(api_key=api_key)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.responses.create(
            model=st.session_state["openai_model"],
            input=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            reasoning={},
            tools=[],
            temperature=0.7,
            max_output_tokens=2048,
            top_p=1,
            store=True
        )
        result = stream.output[0].content[0].text
        st.write(result)
    st.session_state.messages.append({"role": "assistant", "content": result})

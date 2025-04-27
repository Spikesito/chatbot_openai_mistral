from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_image(prompt: str) -> str:
    """Génère une image avec DALL·E 3 et retourne l’URL."""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

def chat_with_openai(messages: list, model: str = "gpt-3.5-turbo") -> str:
    """Envoie une conversation à OpenAI Chat Completions et retourne la réponse."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1
    )
    return response.choices[0].message.content

def chat_with_rag_context(prompt: str, docs: str, model: str = "gpt-3.5-turbo") -> str:
    """Chat avec un contexte RAG injecté en tant que système."""
    response = client.responses.create(
        model=model,
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
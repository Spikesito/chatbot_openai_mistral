from mistralai import Mistral
import streamlit as st

client = Mistral(api_key=st.secrets["MISTRAL_API_KEY"])

def chat_with_mistral_agent(agent_id: str, messages: list[dict], max_tokens: int = 2048) -> str:
    """Envoie un historique de chat à un agent Mistral et récupère la réponse texte."""
    # Nettoyer les messages : ne garder que ceux ayant un vrai content
    cleaned_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in messages
        if isinstance(m["content"], str) and m["content"].strip() != ""
    ]

    response = client.agents.complete(
        agent_id=agent_id,
        messages=cleaned_messages,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content
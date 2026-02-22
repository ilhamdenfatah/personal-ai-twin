import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load knowledge base
def load_knowledge():
    knowledge_text = ""

    ordered_files = [
        "system_prompt.txt",
        "vision.md",
        "thinking_principles.md",
        "personality_rules.md",
        "assistant_behavior.md",
        "response_patterns.md",
        "conversation_rules.md",
        "conversation_examples.md",
        "starter_questions.md",
        "portfolio.md",
        "guardrails.md",
    ]

    for file in ordered_files:
        path = f"knowledge/{file}"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                knowledge_text += f"\n\n{f.read()}"

    return knowledge_text


SYSTEM_CONTEXT = load_knowledge()

# Streamlit UI
st.title("🤖 Ilham AI Twin")
st.caption("Ask anything about Ilham’s experience, projects, or thinking.")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_CONTEXT
            },
            *st.session_state.messages
        ]
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

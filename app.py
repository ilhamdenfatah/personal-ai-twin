import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# =====================================
# 1) Load API key + configure Gemini
# =====================================
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# =====================================
# 2) Load knowledge base
# =====================================
def load_knowledge():
    knowledge_text = ""
    ordered_files = [
        "system_prompt.txt", "vision.md", "thinking_principles.md",
        "personality_rules.md", "assistant_behavior.md", "response_patterns.md",
        "conversation_rules.md", "conversation_examples.md", "starter_questions.md",
        "portfolio.md", "guardrails.md",
    ]
    for file in ordered_files:
        path = f"knowledge/{file}"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                knowledge_text += f"\n\n{f.read()}"
    return knowledge_text

SYSTEM_CONTEXT = load_knowledge()

# =====================================
# 3) Init Gemini Model
# =====================================
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=SYSTEM_CONTEXT
)

# =====================================
# UPGRADE #3 — Sidebar Identity Card
# =====================================
with st.sidebar:
    st.header("About Ilham AI Twin")
    st.write(
        "Ilham AI Twin adalah digital professional twin dari Ilham Den Fatah.\n\n"
        "Anda bisa bertanya tentang:\n"
        "- Latar belakang & journey\n"
        "- Project & portfolio\n"
        "- Cara berpikir / decision mindset\n"
        "- Tools & pendekatan kerja\n"
    )
    st.caption(f"Model: {MODEL_NAME}")

# =====================================
# Streamlit UI
# =====================================
st.title("🤖 Ilham AI Twin")
st.caption("Ask anything about Ilham’s experience, projects, or thinking.")

# =====================================
# Session init
# =====================================
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# UPGRADE #1 — Auto Greeting (UI only)
if "greeted" not in st.session_state:
    st.session_state.greeting_text = (
        "Halo! Saya Ilham AI, digital twin profesional dari Ilham Den Fatah.\n\n"
        "Anda bisa tanya apa pun tentang proyek saya, cara berpikir saya dalam analytics/AI, "
        "atau perjalanan profesional saya. Mau mulai dari mana?"
    )
    st.session_state.greeted = True

# =====================================
# Render chat history
# =====================================
# Tampilkan greeting hanya di UI (tidak masuk history Gemini)
if "greeting_text" in st.session_state and len(st.session_state.chat_session.history) == 0:
    with st.chat_message("assistant"):
        st.markdown(st.session_state.greeting_text)

for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        # Robust: kadang parts bisa >1
        text = ""
        try:
            text = "".join([p.text for p in message.parts if hasattr(p, "text") and p.text])
        except Exception:
            text = str(message)
        st.markdown(text)

# =====================================
# Input
# =====================================
user_input = st.chat_input("Ask something...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # UPGRADE #2 — Streaming / typing effect (rapi & stabil)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            stream = st.session_state.chat_session.send_message(user_input, stream=True)
            for chunk in stream:
                if hasattr(chunk, "text") and chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
        except Exception as e:
            placeholder.markdown(f"⚠️ Gemini error: {e}")
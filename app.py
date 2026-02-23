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
# 2) Load knowledge base (Optimized with Cache)
# =====================================
@st.cache_data # Menghindari re-load file setiap user klik tombol, hemat resource!
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
                knowledge_text += f"\n\n--- FILE: {file} ---\n\n{f.read()}"
    
    # Membatasi context agar tidak melebihi limit token secara efisien
    max_chars = int(os.getenv("MAX_CONTEXT_CHARS", "12000"))
    return knowledge_text[:max_chars]

# Memuat context sekali saja
SYSTEM_CONTEXT = load_knowledge()

# =====================================
# 3) Init Gemini Model
# =====================================
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.0-pro") # Disarankan pake 1.5-flash untuk speed

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=SYSTEM_CONTEXT
)

# =====================================
# Sidebar Identity Card
# =====================================
with st.sidebar:
    st.header("About Ilham AI Twin")
    st.write(
        "Ilham AI Twin adalah digital professional twin dari Ilham Den Fatah.\n\n"
        "Anda bisa bertanya tentang:\n"
        "- Latar belakang & journey\n"
        "- Project & portfolio\n"
        "- Cara berpikir / decision mindset\n"
    )
    st.caption(f"Model: {MODEL_NAME}")
    if st.button("Clear Chat"): # Tambahan fitur reset
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

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

# Auto Greeting
if "greeted" not in st.session_state:
    st.session_state.greeting_text = (
        "Halo! Saya Ilham AI, digital twin profesional dari Ilham Den Fatah.\n\n"
        "Anda bisa tanya apa pun tentang proyek saya, cara berpikir saya dalam analytics/AI, "
        "atau perjalanan profesional saya. Mau mulai dari mana?"
    )
    st.session_state.greeted = True

# =====================================
# Render chat history (Optimized)
# =====================================
if len(st.session_state.chat_session.history) == 0:
    with st.chat_message("assistant"):
        st.markdown(st.session_state.greeting_text)

for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# =====================================
# Input & Streaming Logic (THE FIX)
# =====================================
user_input = st.chat_input("Ask something...")

if user_input:
    # 1. Tampilkan pesan user
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Tampilkan respon bot dengan Streaming yang lebih tangguh
    with st.chat_message("assistant"):
        def response_generator():
            try:
                # Tambahkan timeout parameter jika SDK mendukung, atau biarkan streaming menjaga koneksi
                stream = st.session_state.chat_session.send_message(user_input, stream=True)
                for chunk in stream:
                    if chunk.text:
                        yield chunk.text
            except Exception as e:
                yield f"⚠️ Waduh, ada gangguan koneksi ke 'otak' Gemini saya. Bisa coba lagi? (Error: {str(e)})"

        # Menggunakan st.write_stream untuk UX yang lebih halus dan menjaga heartbeat koneksi
        full_response = st.write_stream(response_generator())
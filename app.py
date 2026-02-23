import os
import re
import time
import random
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ==============================
# 0) Config
# ==============================
st.set_page_config(page_title="Ilham AI Twin", page_icon="🤖", layout="centered")

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Latency controls (bisa diatur di Streamlit Secrets)
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "12000"))  # total retrieval pack
MAX_CHUNK_CHARS = int(os.getenv("MAX_CHUNK_CHARS", "1800"))       # size per chunk
TOP_K_CHUNKS = int(os.getenv("TOP_K_CHUNKS", "4"))               # chunks per query
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "600"))   # smaller = faster
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.4"))

# ==============================
# 1) Load system instruction (KEEP SMALL)
# ==============================
def load_text(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

SYSTEM_INSTRUCTION = load_text("knowledge/system_prompt.txt")
if not SYSTEM_INSTRUCTION:
    SYSTEM_INSTRUCTION = "You are Ilham AI — a professional digital twin of Ilham Den Fatah."

# ==============================
# 2) Knowledge Base (On-demand retrieval)
# ==============================
KB_FILES = [
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

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\u00C0-\u024F\u1E00-\u1EFF\s-]", " ", text)  # keep letters/numbers
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str) -> set:
    t = normalize(text)
    toks = set([w for w in t.split(" ") if len(w) >= 3])
    return toks

def chunk_text(text: str, chunk_size: int = 1800) -> list[str]:
    # Simple chunking by paragraphs, then pack into ~chunk_size char groups
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    buff = ""
    for p in paras:
        if len(buff) + len(p) + 2 <= chunk_size:
            buff = (buff + "\n\n" + p).strip()
        else:
            if buff:
                chunks.append(buff)
            buff = p
    if buff:
        chunks.append(buff)
    return chunks

@st.cache_data(show_spinner=False)
def build_kb_index():
    entries = []
    for fname in KB_FILES:
        path = f"knowledge/{fname}"
        raw = load_text(path)
        if not raw:
            continue
        chunks = chunk_text(raw, chunk_size=MAX_CHUNK_CHARS)
        for i, ch in enumerate(chunks):
            entries.append({
                "file": fname,
                "chunk_id": i,
                "text": ch,
                "tokens": tokenize(ch),
            })
    return entries

KB_INDEX = build_kb_index()

def retrieve_context(query: str) -> str:
    q_tokens = tokenize(query)
    if not q_tokens or not KB_INDEX:
        return ""

    scored = []
    for e in KB_INDEX:
        overlap = len(q_tokens & e["tokens"])
        if overlap > 0:
            scored.append((overlap, e))

    if not scored:
        return ""

    scored.sort(key=lambda x: x[0], reverse=True)
    selected = scored[:TOP_K_CHUNKS]

    # Build context pack with file labels
    pack = []
    total = 0
    for _, e in selected:
        block = f"--- SOURCE: {e['file']} (chunk {e['chunk_id']}) ---\n{e['text']}".strip()
        if total + len(block) > MAX_CONTEXT_CHARS:
            break
        pack.append(block)
        total += len(block)

    return "\n\n".join(pack).strip()

# ==============================
# 3) Model + Chat Session
# ==============================
generation_config = genai.types.GenerationConfig(
    temperature=TEMPERATURE,
    max_output_tokens=MAX_OUTPUT_TOKENS,
)

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=SYSTEM_INSTRUCTION,
    generation_config=generation_config,
)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "greeted" not in st.session_state:
    st.session_state.greeted = True
    st.session_state.chat_session.history.append(
        genai.types.ContentDict(
            role="model",
            parts=[{"text": "Halo! Saya Ilham AI, digital twin profesional dari Ilham Den Fatah.\n\nAnda bisa tanya apa pun tentang proyek saya, cara berpikir saya dalam analytics/AI, atau perjalanan profesional saya. Mau mulai dari mana?"}]
        )
    )

# ==============================
# 4) UI
# ==============================
st.title("Ilham AI Twin")
st.caption("Ask anything about Ilham’s experience, projects, or thinking.")

with st.sidebar:
    st.markdown("### About Ilham AI Twin")
    st.write("Ilham AI Twin adalah digital professional twin dari Ilham Den Fatah.")
    st.write("Anda bisa bertanya tentang:")
    st.markdown("- Latar belakang & journey\n- Project & portfolio\n- Cara berpikir / decision mindset\n- Tools & pendekatan kerja")
    st.caption(f"Model: {MODEL_NAME}")

# Render history
for message in st.session_state.chat_session.history:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

user_input = st.chat_input("Ask something...")

def is_timeout_error(err: Exception) -> bool:
    s = str(err).lower()
    return ("deadline" in s) or ("504" in s) or ("timed out" in s) or ("timeout" in s)

if user_input:
    # Show user msg
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build retrieval context (v2)
    ctx = retrieve_context(user_input)
    if ctx:
        prompt = (
            "Berikut catatan relevan tentang Ilham (gunakan sebagai rujukan utama, jangan mengarang di luar ini):\n\n"
            f"{ctx}\n\n"
            f"Pertanyaan user: {user_input}"
        )
    else:
        prompt = user_input

    # Assistant response with retry + fallback
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                # attempt 1-2: streaming
                if attempt < max_attempts:
                    stream = st.session_state.chat_session.send_message(prompt, stream=True)
                    for chunk in stream:
                        if hasattr(chunk, "text") and chunk.text:
                            full_response += chunk.text
                            placeholder.markdown(full_response + "▌")
                    placeholder.markdown(full_response if full_response else "(No response text returned.)")
                    break

                # last attempt: non-streaming fallback (lebih stabil)
                resp = st.session_state.chat_session.send_message(prompt, stream=False)
                full_response = (getattr(resp, "text", "") or "").strip()
                placeholder.markdown(full_response if full_response else "(No response text returned.)")
                break

            except Exception as e:
                if attempt == max_attempts or not is_timeout_error(e):
                    placeholder.markdown(f"⚠️ Gemini error: {e}")
                    break

                wait = (2 ** attempt) + random.random()
                placeholder.markdown(f"⏳ Gemini sedang padat. Retry {attempt}/{max_attempts-1}...")
                time.sleep(wait)
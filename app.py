import os
import time
import random
import streamlit as st
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# ==============================
# 0) Config
# ==============================
st.set_page_config(
    page_title="Ilham AI Twin",
    page_icon="🤖",
    layout="centered"
)

load_dotenv()

# ==============================
# CONSTANTS
# ==============================
VECTORSTORE_DIR = "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.3-70b-versatile"
TOP_K_CHUNKS = 4
MAX_OUTPUT_TOKENS = 600
TEMPERATURE = 0.4

# ==============================
# AUTO INGEST (untuk Streamlit Cloud)
# ==============================
def run_ingest_if_needed():
    if not os.path.exists(VECTORSTORE_DIR) or not os.listdir(VECTORSTORE_DIR):
        st.info("⏳ Building knowledge base for first time... please wait.")
        
        from langchain_community.document_loaders import DirectoryLoader, TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        import shutil

        # Load
        loader = DirectoryLoader(
            "knowledge",
            glob="**/*.*",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        documents = loader.load()

        # Chunk
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " ", ""],
        )
        chunks = splitter.split_documents(documents)

        # Embed + Store
        embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
        )
        Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=VECTORSTORE_DIR,
        )
        st.success("✅ Knowledge base ready!")
        st.rerun()

run_ingest_if_needed()

# ==============================
# 1) Load system prompt
# ==============================
def load_text(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

SYSTEM_PROMPT = load_text("knowledge/system_prompt.txt")
if not SYSTEM_PROMPT:
    SYSTEM_PROMPT = "You are Ilham AI — a professional digital twin of Ilham Den Fatah."

# ==============================
# 2) Load vectorstore + retriever
# ==============================
@st.cache_resource(show_spinner="Loading knowledge base...")
def load_retriever():
    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
    )
    vectorstore = Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embedding_model,
    )
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K_CHUNKS},
    )
    return retriever

retriever = load_retriever()

# ==============================
# 3) Load Groq LLM
# ==============================
@st.cache_resource(show_spinner=False)
def load_llm():
    return ChatGroq(
        model=GROQ_MODEL,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=TEMPERATURE,
        max_tokens=MAX_OUTPUT_TOKENS,
    )

llm = load_llm()

# ==============================
# 4) Session state
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "greeted" not in st.session_state:
    st.session_state.greeted = True
    greeting = (
        "Hello! I'm Ilham AI, the professional digital twin of "
        "Ilham Den Fatah.\n\n"
        "You can ask me anything about my projects, technical "
        "approach, AI automation work, or professional journey. "
        "Where would you like to start?"
    )
    st.session_state.messages.append({
        "role": "assistant",
        "content": greeting
    })

# ==============================
# 5) UI
# ==============================
st.title("Ilham AI Twin 🤖")
st.caption("Ask anything about Ilham's experience, projects, or thinking.")

with st.sidebar:
    st.markdown("### About Ilham AI Twin")
    st.write(
        "Ilham AI Twin is the professional digital twin of "
        "Ilham Den Fatah."
    )
    st.write("You can explore:")
    st.markdown(
        "- Background & career journey\n"
        "- AI & automation projects\n"
        "- Technical approach & stack\n"
        "- Working philosophy & vision"
    )
    st.caption(f"Model: {GROQ_MODEL}")
    st.caption("Powered by LangChain + ChromaDB + Groq")

# Render chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ==============================
# 6) Chat logic
# ==============================
user_input = st.chat_input("Ask something...")

if user_input:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    # Retrieve relevant chunks from ChromaDB
    docs = retriever.invoke(user_input)
    context = "\n\n".join([
        f"--- SOURCE: {doc.metadata.get('source', 'unknown')} ---\n{doc.page_content}"
        for doc in docs
    ])

    # Build messages for Groq
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=(
            f"Relevant knowledge about Ilham:\n\n{context}\n\n"
            f"User question: {user_input}"
        ))
    ]

    # Generate response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            # Groq streaming
            stream = llm.stream(messages)
            for chunk in stream:
                if chunk.content:
                    full_response += chunk.content
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"⚠️ Error: {e}"
            placeholder.markdown(full_response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })
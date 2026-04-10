# 🤖 Ilham AI Twin — RAG-Powered Professional Digital Twin

🚀 **Live Application:**  
👉 https://ilham-ai-twin.streamlit.app/

---

## Overview

**Ilham AI Twin** is a RAG-powered conversational AI system that represents Ilham Den Fatah's professional identity, projects, and thinking through natural dialogue.

Rather than a static portfolio or generic chatbot, this system is designed as a **digital professional twin** — grounding every response in a structured knowledge base via semantic retrieval, ensuring answers are accurate, consistent, and contextually aware.

Recruiters, hiring managers, and collaborators can explore Ilham's background, projects, technical decisions, and working philosophy through conversation — not by reading a PDF.

---

## 🧠 How It Works — RAG Architecture

This system is built on a **Retrieval-Augmented Generation (RAG)** pipeline, which means the LLM never answers from generic training knowledge alone. Every response is grounded in retrieved context from Ilham's actual knowledge base.

```
INDEXING (runs once on first deployment)
─────────────────────────────────────────
knowledge/*.md files
↓
LangChain RecursiveCharacterTextSplitter
(chunks: 500 chars, overlap: 50)
↓
HuggingFace Embeddings
(sentence-transformers/all-MiniLM-L6-v2)
↓
ChromaDB Vector Store
(persistent local storage)
RETRIEVAL + GENERATION (every user query)
──────────────────────────────────────────
User Query
↓
HuggingFace Embeddings
(embed query → vector)
↓
ChromaDB Similarity Search
(top-4 semantically relevant chunks)
↓
Groq / LLaMA 3.3 70B
(generate grounded response)
↓
Streamlit UI
(streaming response)
```

---

**Why RAG instead of static context injection?**

The previous version of this system loaded all knowledge files 
into the context window on every request — blunt, expensive, and 
unable to scale. The RAG architecture retrieves only the most 
semantically relevant chunks per query, reducing noise and 
improving response quality.

---

## ⚙️ Technical Stack

| Layer | Technology | Role |
|-------|-----------|------|
| Frontend | Streamlit | Conversational UI, streaming |
| Orchestration | LangChain | RAG pipeline, retrieval chain |
| Embedding | HuggingFace (all-MiniLM-L6-v2) | Semantic vector embedding |
| Vector Store | ChromaDB | Persistent similarity search |
| LLM | Groq (LLaMA 3.3 70B) | Response generation |
| Knowledge Base | Structured Markdown | Professional context |

---

## 🗂️ Knowledge Base Structure

The system's behavior is governed by 11 structured knowledge files:

```
knowledge/
├── system_prompt.txt         ← Core identity & behavioral rules
├── vision.md                 ← Professional identity & motivation
├── portfolio.md              ← Project descriptions & decisions
├── thinking_principles.md    ← How Ilham approaches problems
├── assistant_behavior.md     ← Runtime conversation conduct
├── personality_rules.md      ← Tone & communication style
├── guardrails.md             ← Boundaries & truthfulness rules
├── conversation_rules.md     ← Response structure & flow
├── response_patterns.md      ← Adaptive user type handling
├── conversation_examples.md  ← Behavioral reference examples
└── starter_questions.md      ← Suggested entry points
```

Each file is chunked, embedded, and stored in ChromaDB at startup. 
When a user asks a question, only the most relevant chunks are 
retrieved — keeping responses focused and grounded.

---

## 📁 Project Structure

```
personal-ai-twin/
├── knowledge/          ← Knowledge base (11 structured .md files)
├── app.py              ← Main Streamlit app + RAG pipeline
├── ingest.py           ← Standalone ingestion script (local use)
├── requirements.txt    ← Python dependencies
├── .gitignore          ← Excludes vectorstore/, .env
└── README.md
```

**Note:** The `vectorstore/` directory is excluded from Git. 
On first deployment, `app.py` automatically builds the vector 
store from the knowledge files via `run_ingest_if_needed()`.

---

## 🚀 Run Locally

**1. Clone and install**
```bash
git clone https://github.com/ilhamdenfatah/personal-ai-twin.git
cd personal-ai-twin
pip install -r requirements.txt
```

**2. Set up environment**
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

**3. Build the vector store**
```bash
python ingest.py
```

**4. Run the app**
```bash
streamlit run app.py
```

---

## 💡 What This Project Demonstrates

- **RAG pipeline design** — end-to-end: document loading, 
  chunking, embedding, vector storage, semantic retrieval
- **LangChain orchestration** — connecting embeddings, 
  vector store, and LLM into a coherent pipeline
- **Knowledge engineering** — structuring professional context 
  into retrievable, consistent knowledge layers
- **AI behavioral design** — system prompts, guardrails, 
  personality rules, and response patterns working together
- **Production deployment** — auto-ingest on cold start, 
  Streamlit Cloud compatible, zero manual setup required

---

## 🧑🏼‍💼 About the Author

Ilham Den Fatah is an AI Automation Builder & Decision Systems 
Engineer who builds end-to-end systems connecting data pipelines, 
LLM APIs, and workflow automation tools to deliver live business 
intelligence to stakeholders.

This project demonstrates AI not just as automation, but as a 
**communication interface** — a different but equally important 
application pattern.

🔗 GitHub: github.com/ilhamdenfatah  
🔗 LinkedIn: linkedin.com/in/ilham-den-fatah

---

## 🔮 Roadmap

- [ ] Conversation memory across sessions
- [ ] MMR retrieval for more diverse chunk selection
- [ ] Source attribution display in UI
- [ ] Response quality evaluation framework
- [ ] Multi-agent extension for deeper project Q&A
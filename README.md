## 🚧 Deployment Status

This project is fully functional locally.

Live deployment is temporarily disabled due to API billing configuration.
You can run the assistant locally by adding your own OpenAI API key:

1. Create `.env`
2. Add OPENAI_API_KEY
3. Run `streamlit run app.py`

Architecture, prompts, and knowledge system are fully implemented.




# 🤖 Ilham AI Twin — Personal AI Assistant

## Overview

**Ilham AI Twin** is a personal AI assistant designed to represent a professional identity, knowledge system, and thinking approach through conversational interaction.

Instead of functioning as a generic chatbot, this project explores how Large Language Models can be structured to act as a **digital professional twin** — allowing users to understand a person’s experience, projects, and perspectives through natural dialogue.

The assistant answers questions about Ilham’s background, projects, and professional reasoning by grounding responses in curated knowledge files rather than generating generic answers.

This project demonstrates how AI can be applied beyond automation — as a medium for communication, explanation, and decision-oriented interaction.

---

## 🎯 Project Purpose

Recruiters and collaborators often need to understand a candidate across multiple platforms:

- LinkedIn profiles  
- GitHub repositories  
- Portfolio pages  
- Project documentation  

This project experiments with a different approach:

> What if understanding a professional could happen through conversation instead of navigation?

Ilham AI Twin allows users to directly ask:

- What problems has Ilham worked on?
- How does he approach analytics and AI?
- What kind of decisions does he care about solving?
- How does he think about business and data?

The assistant responds using structured context rather than static summaries.

---

## 🧠 Core Concept

The system is built around a **knowledge-driven architecture**, where behavior and responses are guided by layered context:

System Identity
↓
Thinking Principles
↓
Personality Rules
↓
Conversation Behavior
↓
Project & Vision Knowledge
↓
LLM Response


Rather than relying solely on prompts, the assistant integrates multiple knowledge layers to maintain consistency, reasoning style, and professional tone.

---

## ⚙️ Technical Architecture

### Frontend
- Streamlit conversational interface

### AI Layer
- OpenAI GPT model
- Context-driven system prompt
- Persistent conversational memory

### Knowledge System
Structured markdown-based knowledge files:

- Vision & professional identity
- Portfolio explanations
- Thinking principles
- Behavioral rules
- Conversation examples
- Guardrails & response patterns

All knowledge files are dynamically loaded and combined into a unified system context at runtime.

---

## 💡 What This Project Demonstrates

This project highlights capabilities relevant to modern data and AI roles:

- Designing AI systems beyond simple API usage
- Prompt architecture and behavioral alignment
- Translating professional experience into conversational interfaces
- Decision-oriented explanation design
- Applied AI thinking for real-world communication problems

---

## 🚧 Deployment Status

This project is fully functional locally.

Live deployment is temporarily disabled due to API billing configuration.  
You can run the assistant locally by adding your own OpenAI API key:

1. Create `.env`
2. Add `OPENAI_API_KEY`
3. Run:

```bash
streamlit run app.py
```

---

## Running Locally

git clone https://github.com/your-username/ilham-ai-assistant.git
cd ilham-ai-assistant
pip install -r requirements.txt
streamlit run app.py

---

📁 Project Structure

```
knowledge/
├── system_prompt.txt
├── vision.md
├── portfolio.md
├── thinking_principles.md
├── personality_rules.md
├── assistant_behavior.md
├── conversation_rules.md
├── response_patterns.md
├── conversation_examples.md
└── guardrails.md
```

## About the Author

Ilham is a data practitioner transitioning toward Business Data Analytics and Applied Data Science, with a strong interest in decision-oriented analytics and AI-driven systems.

This project reflects an exploration of how analytics, AI, and human reasoning can be combined into practical and understandable tools.

## Future Direction

Potential future improvements include:
- Live deployment environment
- Retrieval-based knowledge expansion
- Memory persistence
- Multi-agent interaction experiments
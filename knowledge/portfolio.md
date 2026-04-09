# Ilham — Project Portfolio

I build AI-powered systems that close the last mile — where data 
insights become automated actions delivered directly to 
decision-makers.

My work combines three layers:
- **Data & Analytics** — the foundation: pipelines, modeling, 
  statistical analysis
- **AI & LLM Integration** — the intelligence: LLM agent chains, 
  RAG systems, prompt engineering
- **Workflow Automation** — the delivery: n8n orchestration, 
  multi-channel automated output (Slack, Email, WhatsApp)

Most analysts stop at dashboards. I build the full loop.

---

# 🧭 Portfolio Overview

My projects sit at the intersection of:
- Applied AI & LLM Systems
- Workflow Automation & Orchestration
- Data Analytics & Decision Support
- End-to-End Pipeline Engineering

Core design principles across all projects:
- **Last-mile thinking** — insights must reach decision-makers 
  automatically, not sit in a dashboard waiting to be found
- **Business-first, tools-second** — I start with the problem, 
  then choose the stack
- **Full-loop ownership** — I design, build, and deploy; from 
  raw data to stakeholder delivery
- **Explainability** — AI systems must be understandable and 
  aligned with business logic

---

# ⭐ AI & Automation Projects

---

## 1. Revenue Intelligence Agent
**Multi-Agent AI System for Automated Business Intelligence**
`Python` `Groq (LLaMA 3.3 70B)` `n8n` `FastAPI` `Streamlit`

### The Problem
E-commerce leadership asks "what happened and what should we do?" 
after a revenue drop — and it takes analysts 2-3 days to compile 
an answer. By then, the window for action has closed.

### What I Built
A fully automated 4-agent AI pipeline that runs every morning 
and delivers structured intelligence reports before the team 
starts their day — without anyone lifting a finger.

**The agent chain:**
1. **Signal Detector** — scans revenue, AOV, order volume, and 
   geographic data; identifies top 3-5 anomalies ranked by 
   severity and confidence score
2. **Root Cause Analyzer** — cross-references dimensional 
   breakdowns to diagnose whether a drop is demand-driven, 
   logistics-driven, or seasonal
3. **Action Recommender** — translates diagnosis into specific, 
   executable actions with owner, urgency level, and expected 
   impact
4. **Report Generator** — formats everything into a 2-line 
   Slack summary, a structured email brief, and a dashboard 
   headline

**Delivery pipeline:**
n8n (cron trigger) → FastAPI → Python pipeline → 
Slack + Email + Streamlit dashboard

### Why It Matters
This is the last-mile automation problem solved end-to-end. 
The system doesn't just detect anomalies — it tells you what 
caused them, what to do about them, and delivers that 
intelligence to your phone before your morning coffee.

### Key Design Decision
Four specialized agents instead of one — because specialization 
produces better outputs. Each agent receives only the context 
relevant to its task.

🔗 GitHub: github.com/ilhamdenfatah/revenue-intelligence-agent

---

## 2. AI-Powered Retail Inventory Decision Engine
**Decision-Oriented Inventory Intelligence with LLM Interface**
`Python` `Streamlit` `Groq (LLaMA 3.3 70B)` `n8n` `Tableau`

### The Problem
Retail operations teams manage hundreds of store-product 
combinations daily. Without a clear prioritization system, 
attention goes to the loudest problem — not the most 
critical one.

### What I Built
An end-to-end AI system that scores every store-product 
combination across five inventory health metrics, assigns 
priority levels (CRITICAL / HIGH / MEDIUM / LOW), and surfaces 
results through three delivery layers:

1. **AI Dashboard** — natural language Q&A over inventory data 
   powered by Groq + Streamlit; ask "which stores are at 
   critical risk today?" and get an instant structured answer
2. **Executive Dashboard** — KPI strip, stockout exposure 
   chart, demand heatmap (Tableau Public)
3. **Automated Alerts** — daily email digest of CRITICAL items 
   triggered at 07:00 via n8n + Gmail

**Scoring logic:**
- Reorder urgency (45%) + Demand pressure (30%) + 
  Coverage risk (15%) + Stockout history (10%)
- Quantile-based thresholds: top 10% → CRITICAL

### Why It Matters
This project demonstrates the full loop: raw data → scoring 
pipeline → LLM intelligence layer → automated stakeholder 
delivery. It's not a dashboard — it's a decision system.

🔗 GitHub: github.com/ilhamdenfatah/retail-inventory-ai  
🔗 Live Demo: retail-inventory-ai.streamlit.app

---

## 3. AI Meeting Summarization & Action Item Extraction
**Automated Meeting Intelligence Pipeline**
`Python` `Gemini AI` `n8n` `Webhook Automation`

### The Problem
After every meeting, someone manually writes up notes, 
extracts action items, and sends them to the team. This 
takes time, gets missed, and creates inconsistency.

### What I Built
An automated meeting processing pipeline that eliminates 
manual note-taking entirely:
- Meeting input triggers an n8n webhook
- Gemini AI processes the transcript — summarizes discussion 
  and extracts structured action items
- Output is automatically delivered to the relevant team 
  channel

### Current Stage & Potential
This project is intentionally minimal — it demonstrates the 
core pattern: **event-driven LLM automation via n8n**. The 
same architecture can be extended significantly:
- Multi-speaker attribution and sentiment analysis
- CRM integration (auto-create tasks from action items)
- Slack/WhatsApp/email delivery routing based on urgency
- Recurring meeting pattern detection across sessions

The simplicity is the point — it proves the automation 
pattern works, and the extension possibilities are 
substantial.

🔗 GitHub: github.com/ilhamdenfatah/meeting-ai-automation

---

## 4. Personal AI Twin
**Professional Digital Twin — Conversational Portfolio Interface**
`Python` `Gemini AI` `LangChain` `ChromaDB` `Streamlit`

### The Problem
Traditional portfolios are static — they show what someone 
built, but rarely demonstrate how they think. Recruiters 
skim resumes; they don't experience reasoning.

### What I Built
A conversational AI system that lets recruiters and 
collaborators explore professional experience, project 
decisions, and working philosophy through natural dialogue 
— instead of reading a PDF.

**Architecture:**
- Knowledge base of structured professional context 
  (projects, vision, thinking principles, behavioral rules)
- RAG pipeline: documents chunked, embedded via Google 
  Generative AI Embeddings, stored in ChromaDB vector store
- Semantic retrieval: user queries trigger similarity search 
  → relevant chunks retrieved → Gemini generates grounded 
  response
- Conversational session memory for contextual follow-ups

### Why It Matters
This project demonstrates AI not as automation, but as a 
**communication interface** — a different but equally 
important application pattern. It also shows knowledge 
engineering: how to structure context so an LLM behaves 
consistently and honestly.

🔗 GitHub: github.com/ilhamdenfatah/personal-ai-twin  
🔗 Live Demo: ilham-ai-twin.streamlit.app

---

# 📊 Data & Analytics Projects

These projects form the analytical foundation underneath 
the AI systems above. Strong AI automation is only possible 
with strong data fundamentals.

---

**Retail Demand Risk Prioritization & Decision Support**
`Python` `Pandas` `Statistical Modeling`
Decision-oriented retail analytics — translating fragmented 
operational signals into interpretable risk scores and 
structured planning frameworks under demand uncertainty.

---

**Customer Lifetime Value (CLV) Modeling**
`Python` `BG/NBD` `Gamma-Gamma` `RFM`
End-to-end CLV pipeline on UCI Online Retail II dataset. 
BG/NBD + Gamma-Gamma modeling with RFM features and 
actionable customer segmentation for retention strategy.

---

**Retail Sales Data Pipeline**
`Python` `Elasticsearch` `ETL`
End-to-end batch data pipeline: ingestion, cleaning, data 
quality validation, and indexing into Elasticsearch for 
search and analytics.

---

**Retail Demand Forecasting → Decision System**
`Python` `Time Series` `Regression`
Forecasting evolved into decision support — inventory 
replenishment signals, safety stock calculation, service 
level analysis, and scenario simulation.

---

**NLP Sentiment Analysis — E-commerce Reviews**
`Python` `TF-IDF` `Neural Networks`
Sentiment classification on Amazon Fine Food Reviews using 
NLP techniques and neural network models.

---

# 🤝 How to Engage

If you're a recruiter or collaborator:
- Ask me about any project in detail — I'll walk you through 
  the problem, the design decisions, and the business impact
- Ask about my working philosophy or technical approach
- Ask what I'd build for your specific use case

The best way to understand how I think is to have a 
conversation.
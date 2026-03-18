<div align="center">

  <img src="https://raw.githubusercontent.com/endee-io/endee/main/docs/assets/logo-dark.svg" height="70" alt="Endee Logo" />

  <br><br>

  <h1>🔥 Errorlens AI</h1>
  <h3>An Intelligent, RAG-Powered Semantic Debugging Assistant</h3>

  <p>
    <b>Engineered exclusively for the Endee.io Project-Based Evaluation</b>
  </p>

  <p>
    <a href="#live-demo"><img src="https://img.shields.io/badge/Live_Demo-Active-6C5CE7?style=for-the-badge&logo=vercel" alt="Live Demo" /></a>
    <img src="https://img.shields.io/badge/Vector_DB-Endee-00B894?style=for-the-badge&logo=databricks" alt="Endee" />
    <img src="https://img.shields.io/badge/AI_Engine-Google_Gemini-FDCB6E?style=for-the-badge&logo=google" alt="Gemini" />
    <img src="https://img.shields.io/badge/Backend-FastAPI-0984E3?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  </p>
</div>

---

## 🙏 A Message to the Endee Team

First and foremost, **thank you** for this incredible opportunity to evaluate the Endee Vector Database. Building Errorlens AI was an absolute thrill. Endee's under-the-hood C++ optimizations, blazing-fast HNSW indexing, and highly elegant Python SDK made engineering this Retrieval-Augmented Generation (RAG) pipeline an incredibly seamless experience. 

This assignment reinforced exactly why high-performance edge vector search is the future of intelligent tooling. Thank you for your vision and for empowering developers to build smarter applications.

---

## 🎬 See it in Action!

Watch the complete Endee RAG pipeline run in real-time.

<div align="center">
  <video src="ErrorLense_ai.mp4" autoplay loop muted playsinline width="100%" controls></video>
  <br>
  <i>(If the video doesn't automatically load, please click the <b>ErrorLense_ai.mp4</b> file directly in the repository to view it in high definition!)</i>
</div>

---

## 🚀 Live Demo Link

Feel free to interact with the production deployment here:  
👉 **[View Live Demo of Errorlens AI](#)** *(Replace this `#` with your actual Render/Vercel URL if hosted!)*

---

## 💡 What is Errorlens AI?

Developers waste countless hours deciphering cryptic, ambiguous error traces. **Errorlens AI** changes the entire debugging paradigm by looking past exact-keyword matching and actually understanding the **semantic intent** of a crash.

When a developer pastes a stack trace into the UI, Errorlens:
1. **Encodes** the text into a 384-dimensional semantic float vector via `Sentence Transformers`.
2. **Searches** the **Endee Vector Database** instantly locating the absolute closest historical error-solution pairs using cosine similarity.
3. **Generates** a custom fix by feeding the exact Endee matches into **Google Gemini 2.0 Auto/RAG**, generating a stunning HTML/CSS struct containing a Root Cause Analysis, Step-By-Step Solution, and perfectly highlighted Code Tabs.

### 🌟 Multi-Language Support
Errorlens natively supports **8 ecosystems** featuring over **720+ manually curated data patterns** stored actively inside Endee:
- **Languages:** Python (200+), Java (180+), JavaScript (250+)
- **Databases:** MySQL (42), MongoDB (21), Redis (10), Firebase (10), Cassandra (5)

---

## 🏗️ System Design & Architecture

```text
┌────────────────────────────────────────────────────────┐
│                   ERRORLENS AI                         │
│                                                        │
│  User Input (Error Trace)                              │
│         │                                              │
│         ▼                                              │
│  ┌──────────────────────────────────────────┐          │
│  │             FastAPI Backend              │          │
│  │                                          │          │
│  │  1. /search ──► Embed ──► Endee Query    │          │
│  │  2. /rag    ──► Context + LLM ──► Report │          │
│  └──────┬──────────────────────┬────────────┘          │
│         │                      │                       │
│         ▼                      ▼                       │
│  ┌──────────────┐      ┌──────────────┐                │
│  │ Endee Vector │      │ Google       │                │
│  │ Database     │      │ Gemini AI    │                │
│  │ (Docker)     │      │ (RAG Engine) │                │
│  └──────────────┘      └──────────────┘                │
│         │                      │                       │
│         ▼                      ▼                       │
│   Semantic Matches + Structured HTML/JSON Debug Output │
└────────────────────────────────────────────────────────┘
```
**Why Endee was perfect for this:** It provides incredibly rapid, sub-millisecond retrieval of highly dimensional integer/float arrays at scale, which operates beautifully when doing real-time typing/querying against large LLMs. 

---

## ⚙️ Quick Setup Instructions

Want to run Errorlens AI locally? Follow these steps:

**1. Clone this repository**
```bash
git clone https://github.com/ashokkumarboya93/endee.git
cd endee
```

**2. Start Endee Vector Database**
```bash
# Spin up the provided C++ Endee Database inside Docker
docker compose up -d
```

**3. Setup Python & Dependencies**
```bash
cd debugbot
python -m venv venv
# Activate it (Window: .\venv\Scripts\activate | Mac/Linux: source venv/bin/activate)

pip install -r requirements.txt
```

**4. Configure AI Engine**  
Create a `.env` file inside `debugbot/api/` and add your free Google AI API Key:
```env
GEMINI_API_KEY=your_google_gemini_key_here
```

**5. Ingest the Data to Endee**
```bash
# Converts the 700+ CSV parameters into Vector Embeddings and saves to Endee
python -m ingest.loader
```

**6. Launch!**
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
Navigate to **`http://localhost:8000`** in any browser.

---

<div align="center">
  <b>Errorlens AI</b> &copy; 2026 — Built by Ashok Kumar Boya<br>
  <i>Semantic AI Debugging · RAG Pipeline · Vector Search</i>
</div>

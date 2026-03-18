<p align="center">
  <img height="100" alt="Endee" src="./docs/assets/logo-dark.svg">
</p>


<div align="center">

<!-- HERO BANNER -->
<img src="./docs/assets/logo-dark.svg" height="90" alt="Endee Logo" />

<br/>

# 🙏 A Note of Gratitude — Thank You, Endee

> *"Endee didn't just power our search — it gave this project a brain."*

**Errorlens AI** was built on top of the **[Endee Vector Database](https://github.com/endee-io/endee)** — a blazing-fast, C++-native vector engine with HNSW indexing, cosine similarity, and an elegant Python SDK. Without Endee's performance, reliability, and developer-first design, a production-grade RAG debugging system like this would not have been possible.

Thank you, Endee team — for building tools that let developers build *smarter*. 💙

---

<br/>

<!-- TITLE BLOCK -->

<h1>
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=36&pause=1000&color=6366F1&center=true&vCenter=true&width=700&lines=Errorlens+AI;Semantic+Debug+Report+Generator;RAG+%2B+Vector+Search+%2B+AI" alt="Typing SVG" />
</h1>

<p align="center">
  <strong>An intelligent, RAG-powered debugging assistant that understands your errors <em>semantically</em> — and turns them into structured, actionable debug reports.</strong>
</p>

<br/>

<!-- BADGES -->
<p align="center">
  <img src="https://img.shields.io/badge/Endee-Vector%20DB-6366F1?style=for-the-badge&logo=databricks&logoColor=white" />
  <img src="https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Sentence%20Transformers-NLP-FF6B35?style=for-the-badge&logo=huggingface&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/700%2B-Error%20Patterns-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/8-Languages%20%26%20DBs-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/%3C2s-Report%20Generation-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge" />
</p>

<br/>

<!-- DEMO LINKS -->
<p align="center">
  <a href="https://drive.google.com/drive/folders/1nU9-94BDw6loG4h13a26zZpXXY5a6FXK?usp=sharing">
    <img src="https://img.shields.io/badge/🚀%20Live%20Demo-View%20on%20Google%20Drive-6366F1?style=for-the-badge&logo=googledrive&logoColor=white" alt="Live Demo" />
  </a>
  &nbsp;&nbsp;
  <a href="#-demo-video">
    <img src="https://img.shields.io/badge/▶%20Watch%20Demo-Video%20Walkthrough-FF0000?style=for-the-badge&logo=googledrive&logoColor=white" alt="Watch Video" />
  </a>
</p>

</div>

---

## 📺 Demo Video

<div align="center">

> 🎬 **Watch Errorlens AI in action** — from pasting an error to receiving a full structured debug report in under 2 seconds.

[![▶ Click to Watch — Full Demo Video](https://img.shields.io/badge/▶%20Click%20to%20Watch-Full%20Demo%20on%20Google%20Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/drive/folders/1nU9-94BDw6loG4h13a26zZpXXY5a6FXK?usp=sharing)

📂 **[Open Demo Folder on Google Drive](https://drive.google.com/drive/folders/1nU9-94BDw6loG4h13a26zZpXXY5a6FXK?usp=sharing)** — includes the full walkthrough video and screenshots.

</div>

---

## ✨ What is Errorlens AI?

When a developer pastes an error — a stack trace, a cryptic exception, a vague description — **Errorlens AI doesn't just keyword-match.** It *understands.*

```
"object is null"  →  matches  →  NullPointerException
                    (zero words overlap, but semantically identical)
```

Here's what happens under the hood:

```
Your Error String
      │
      ▼
┌─────────────────────────────────────────────┐
│  Phase 1 — Semantic Search                 │
│  Encode → 384-dim vector → Query Endee DB  │
│  Return Top-K similar error patterns        │
└─────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────┐
│  Phase 2 — RAG Report Generation           │
│  Context + Query → Google Gemini 2.0        │
│  Parse structured JSON → Render Report      │
└─────────────────────────────────────────────┘
      │
      ▼
🎯 Full Debug Report: Root Cause · Fix · Code · Tips · Links
```

---

## 🔥 Key Features

<table>
<tr>
<td width="50%">

### 🧠 Semantic Search (NLP)
- Meaning-based matching via `all-MiniLM-L6-v2`
- 384-dimensional vector embeddings
- Sub-second retrieval via Endee's **HNSW indexing**
- No keyword overlap required

</td>
<td width="50%">

### 📄 RAG Report Generation
- Structured JSON reports via **Google Gemini 2.0 Flash**
- Root cause · Description · Solution · Code examples
- Auto-generated documentation reference links
- Keyword highlighting throughout the report

</td>
</tr>
<tr>
<td width="50%">

### 🌐 8 Languages & Databases
- **Python, Java, JavaScript** — 630+ patterns
- **MySQL, MongoDB, Redis** — all major DB flavors
- **Firebase, Cassandra** — cloud & distributed DBs
- Language-specific code examples in every report

</td>
<td width="50%">

### 🛡️ Intelligent Fallback System
- Never fails — even without Gemini API quota
- Fallback generator creates equally detailed reports
- Language-aware code patterns for all 8 platforms
- Graceful degradation with full feature parity

</td>
</tr>
<tr>
<td width="50%">

### 🎨 Beautiful Web UI
- Toon-flat professional landing page
- Live debug console with loading animation
- Multi-section report cards with color-coded stripes
- Developer profile page with social links

</td>
<td width="50%">

### 📤 Export Options
- **JSON** structured export
- **TXT** plain-text download
- **Copy to Clipboard** with toast notification
- All report sections included in every export

</td>
</tr>
</table>

---

## 🗂️ Supported Languages & Error Patterns

<div align="center">

| Platform | Patterns | Type |
|:--------:|:--------:|:----:|
| 🐍 **Python** | 200+ | Programming Language |
| ☕ **Java** | 180+ | Programming Language |
| 🟨 **JavaScript** | 250+ | Programming Language |
| 🐬 **MySQL** | 42 | Relational Database |
| 🍃 **MongoDB** | 21 | NoSQL Database |
| 🔴 **Redis** | 10 | In-Memory Store |
| 🔥 **Firebase** | 10 | Cloud Platform |
| 👁️ **Cassandra** | 5 | Distributed Database |

</div>

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ERRORLENS AI                          │
│                                                         │
│  ┌──────────┐   ┌──────────────────┐   ┌─────────────┐ │
│  │ Landing  │   │  Debug Console   │   │  Developer  │ │
│  │  Page    │   │  (Input+Report)  │   │   Profile   │ │
│  └──────────┘   └────────┬─────────┘   └─────────────┘ │
│                          │                               │
│  ┌───────────────────────▼───────────────────────────┐  │
│  │                FastAPI Backend                     │  │
│  │  POST /search ──► Embed ──► Endee Query           │  │
│  │  POST /rag    ──► Context + LLM ──► Report        │  │
│  └───────────────┬──────────────┬─────────────────────┘  │
│                  │              │                         │
│                  ▼              ▼                         │
│     ┌──────────────┐   ┌──────────────┐                  │
│     │ Endee Vector │   │ Google       │                  │
│     │ Database     │   │ Gemini 2.0   │                  │
│     │ HNSW · 384d  │   │ RAG Reports  │                  │
│     └──────────────┘   └──────────────┘                  │
└─────────────────────────────────────────────────────────┘
```

---

## ⚙️ Tech Stack

<div align="center">

| Layer | Technology | Role |
|:-----:|:----------:|:----:|
| 🗄️ Vector DB | **Endee** (C++ HNSW) | Semantic similarity search |
| 🔧 Backend | **FastAPI** (Python) | REST API + static serving |
| 🤖 Embeddings | **all-MiniLM-L6-v2** | Text → 384-dim vectors |
| 🧬 LLM | **Google Gemini 2.0 Flash** | RAG report generation |
| 🖼️ Frontend | **HTML + CSS + Vanilla JS** | No framework — pure & fast |
| 🐳 DevOps | **Docker Compose** | Endee vector DB container |
| 🔤 Fonts | **Plus Jakarta Sans + JetBrains Mono** | Professional typography |

</div>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker Desktop
- Google Gemini API Key *(free)*

### 1. Clone & Start Endee

```bash
git clone https://github.com/ashokkumarboya93/endee.git
cd endee
docker compose up -d
```

### 2. Install Dependencies

```bash
cd debugbot
python -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Key

```bash
# Create debugbot/api/.env
echo "GEMINI_API_KEY=your_key_here" > api/.env
```

> 🔑 Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey)

### 4. Ingest Error Data

```bash
python -m ingest.loader
```

```
✅ Processing python_errors.csv     →  200+ patterns
✅ Processing java_errors.csv       →  180+ patterns
✅ Processing javascript_errors.csv →  250+ patterns
✅ Processing sql_errors.csv        →   93 patterns
🚀 723 vectors upserted to Endee!
```

### 5. Launch the App

```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

<div align="center">

| Page | URL |
|:----:|:---:|
| 🏠 Landing Page | `http://localhost:8000` |
| 🐛 Debug Console | `http://localhost:8000/debug` |
| 📖 API Docs | `http://localhost:8000/docs` |

</div>

---

## 📊 Example Queries

<details>
<summary><strong>🐍 Python — IndexError</strong></summary>

**Input:** `IndexError: list index out of range`

**Report includes:**
- Root cause: accessing beyond list boundaries
- Code: `len()` validation, `try/except IndexError`, safe indexing patterns
- Reference: docs.python.org/3/library/exceptions.html

</details>

<details>
<summary><strong>☕ Java — NullPointerException</strong></summary>

**Input:** `NullPointerException: Cannot invoke method on null object`

**Report includes:**
- Root cause: dereferencing a null reference
- Code: null checks, `Optional<>`, `Objects.requireNonNull()`
- Reference: docs.oracle.com/javase/8/docs/api/java/lang/NullPointerException.html

</details>

<details>
<summary><strong>🟨 JavaScript — TypeError</strong></summary>

**Input:** `TypeError: Cannot read properties of undefined (reading 'map')`

**Report includes:**
- Root cause: calling `.map()` on an undefined variable
- Code: optional chaining `?.`, `Array.isArray()`, nullish coalescing `??`

</details>

<details>
<summary><strong>🐬 MySQL — Deadlock</strong></summary>

**Input:** `Deadlock Detected: Transactions blocking each other`

**Report includes:**
- Root cause: circular lock dependency between concurrent transactions
- Code: consistent lock ordering, `FOR UPDATE`, retry logic

</details>

---

## 📁 Project Structure

```
endee/
├── debugbot/
│   ├── api/
│   │   ├── main.py              # FastAPI backend
│   │   └── .env                 # GEMINI_API_KEY
│   ├── data/
│   │   ├── python_errors.csv    # 200+ Python patterns
│   │   ├── java_errors.csv      # 180+ Java patterns
│   │   ├── javascript_errors.csv# 250+ JS patterns
│   │   └── sql_errors.csv       # 93 DB patterns
│   ├── ingest/
│   │   └── loader.py            # CSV → Endee vectors
│   ├── website/
│   │   ├── index.html           # Landing page
│   │   ├── debug.html           # Debug console
│   │   └── debug.js             # Frontend logic
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 🛣️ Roadmap

- [ ] 🔄 **Continuous Learning** — auto-ingest new errors from user queries
- [ ] 🔀 **Hybrid Search** — dense vectors + sparse BM25 keyword matching
- [ ] 📸 **Multi-Modal Input** — screenshot error messages with OCR
- [ ] 🔁 **CI/CD Plugin** — GitHub Actions integration to auto-debug builds
- [ ] 📡 **Live Monitoring** — real-time error stream analysis from logs
- [ ] 🌙 **Dark Mode** — full dark theme across all pages
- [ ] 👤 **User Auth** — personal error history and saved reports

---

## 🙌 Acknowledgements

<div align="center">

| Technology | Role |
|:----------:|:----:|
| [**Endee Vector Database**](https://github.com/endee-io/endee) | Semantic vector search — the heart of this project |
| [**Google Gemini AI**](https://ai.google.dev) | LLM for RAG report generation |
| [**Sentence Transformers**](https://www.sbert.net) | `all-MiniLM-L6-v2` text embeddings |
| [**FastAPI**](https://fastapi.tiangolo.com) | Backend REST API framework |
| [**Plus Jakarta Sans**](https://fonts.google.com/specimen/Plus+Jakarta+Sans) | Primary UI typeface |
| [**JetBrains Mono**](https://www.jetbrains.com/lp/mono/) | Code typography |

</div>

---

<div align="center">

### 💙 Special Thanks to Endee

> The **Endee Vector Database** is the backbone of Errorlens AI.  
> Its high-performance C++-based architecture, HNSW indexing, cosine similarity support,  
> and elegant Python SDK made it possible to build a **production-grade RAG system**  
> with remarkable speed and reliability.  
>
> *This project wouldn't exist without the vision and technology that Endee brings to the ecosystem.*  
> **Thank you for empowering developers to build smarter.** 🚀

<br/>

---

**Errorlens AI** &copy; 2026 — Built by [Ashok Kumar Boya](https://github.com/ashokkumarboya93)

*Semantic AI Debugging · RAG Pipeline · Vector Search*

<br/>

⭐ **If this project helped you, please give it a star!** ⭐

</div>

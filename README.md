<p align="center">
  <img height="100" alt="Endee" src="./docs/assets/logo-dark.svg">
</p>

# Errorlens AI — Semantic Debug Report Generator

**An AI/ML project built with Endee Vector Database for the Endee.io Project-Based Evaluation.**

> Built with **Endee Vector Database** · **Google Gemini AI** · **Sentence Transformers** · **FastAPI**

---

## 🎯 Endee Project Evaluation Criteria Addressed
- ✅ **Built an AI/ML project using Endee** as the core vector database for semantic search.
- ✅ **Practical Use Case:** Demonstrates Semantic Search and Retrieval-Augmented Generation (RAG) to instantly retrieve context-aware bug fixes.
- ✅ **Clear README:** Includes project overview, system design, use of Endee, and setup instructions.
- ✅ **Hosted on GitHub:** Hosted in my personal, starred, and forked repository.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Key Features](#2-key-features)
3. [System Architecture (System Design)](#3-system-architecture-system-design)
4. [Technology Stack](#4-technology-stack)
5. [Supported Languages & Databases](#5-supported-languages--databases)
6. [Project Structure](#6-project-structure)
7. [Setup & Installation Instructions](#7-setup--installation-instructions)
8. [Running the Application](#8-running-the-application)
9. [How It Works — The RAG Pipeline](#9-how-it-works--the-rag-pipeline)
10. [Debug Report Structure](#10-debug-report-structure)
11. [API Endpoints](#11-api-endpoints)
12. [Data Ingestion](#12-data-ingestion)
13. [Example Queries](#13-example-queries)
14. [Use of Endee (Why Endee?)](#14-use-of-endee-why-endee)
15. [Acknowledgements](#15-acknowledgements)

---

## 1. Overview

**Errorlens AI** is a full-stack AI debugging assistant that goes far beyond simple keyword matching. When a developer pastes an error message, stack trace, or describes an issue, Errorlens AI:

1. **Embeds** the error text into a 384-dimensional semantic vector using Sentence Transformers.
2. **Searches** the Endee Vector Database for the most similar known error patterns using cosine similarity.
3. **Generates** a comprehensive, structured debug report using Google Gemini AI (RAG) or an intelligent fallback system.
4. **Presents** the report in a beautiful, exportable format with code examples, reference links, and prevention tips.

The application supports **8 languages and databases**: Python, Java, JavaScript, MySQL, MongoDB, Redis, Firebase, and Cassandra — with **720+ curated error patterns** actively indexed in the Endee base.

---

## 2. Key Features

### Semantic Search (NLP)
- **Meaning-based matching** — finds errors based on semantic similarity, not keyword overlap.
- *"object is null"* correctly matches *"NullPointerException"* even though zero words overlap.
- Sub-second High-Dimensional retrieval via Endee's fast HNSW indexing algorithm.

### RAG Report Generation (LLM)
- **Structured debug reports** with root cause, description, solution, code examples, and prevention tips.
- **Language-specific code samples** — both erroneous and corrected code.
- **Graceful fallback** — when the LLM quota is exhausted, a rich, deterministic fallback generator produces equally detailed reports to ensure maximum uptime.

### Modern Web UI
- **Landing page** — animated concepts explaining Semantic Search, RAG concepts, architecture, and tech features.
- **Debug console** — user input area with dynamic multi-language tabs.
- **Export options** — Download to JSON, copy directly to the clipboard.

---

## 3. System Architecture (System Design)

```
┌─────────────────────────────────────────────────────────┐
│                    ERRORLENS AI                          │
│                                                         │
│  ┌──────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │ Landing  │     │ Debug Console│     │ Developer   │ │
│  │ Page     │     │ (Input +     │     │ Profile     │ │
│  │          │     │  Report)     │     │ Page        │ │
│  └──────────┘     └──────┬───────┘     └─────────────┘ │
│                          │                               │
│         ┌────────────────┼────────────────┐              │
│         │                │                │              │
│         ▼                ▼                ▼              │
│  ┌─────────────────────────────────────────────┐        │
│  │              FastAPI Backend                 │        │
│  │                                              │        │
│  │  POST /search ──► Embed ──► Endee Query     │        │
│  │  POST /rag    ──► Context + LLM ──► Report  │        │
│  │  GET  /       ──► Landing Page              │        │
│  │  GET  /debug  ──► Debug Console             │        │
│  └──────────┬──────────────┬───────────────────┘        │
│             │              │                             │
│             ▼              ▼                             │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │ Endee Vector │  │ Google       │                     │
│  │ Database     │  │ Gemini AI    │                     │
│  │ (Docker)     │  │ (gemini-2.0) │                     │
│  │              │  │              │                     │
│  │ HNSW Index   │  │ RAG Context  │                     │
│  │ 384-dim      │  │ Generation   │                     │
│  │ Cosine Sim   │  │              │                     │
│  └──────────────┘  └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
```

The system is decoupled directly into two specific operations:
1. **The Vector Search Phase:** Uses `all-MiniLM-L6-v2` locally inside FastAPI to build query vectors. Endee performs nearest neighbor lookup.
2. **The Generation Phase:** The Top-K items from Endee form the semantic context window, securely passed alongside the original traceback to Google Gemini for structural completion.

---

## 4. Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Vector Database** | Endee (C++ HNSW Engine) | High-performance semantic similarity search |
| **Backend API** | FastAPI (Python) | REST endpoints for search, RAG, and static file serving |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 | Converts text → 384-dimensional vectors |
| **LLM** | Google Gemini 2.0 Flash | Generates structured debug reports via RAG |
| **Frontend** | Vanilla HTML/CSS/JS | Lightning-fast static application interface |
| **Containerization** | Docker Compose | Runs the Endee vector database safely in isolation |

---

## 5. Supported Languages & Databases

- **Programming:** Python (200+ patterns), Java (180+ patterns), JavaScript (250+ patterns)
- **Databases/Misc:** MySQL (42), MongoDB (21), Redis (10), Firebase (10), Cassandra (5)

---

## 6. Project Structure

```
endee/
├── debugbot/
│   ├── api/
│   │   ├── main.py              # FastAPI endpoints (The Core Application)
│   │   └── .env                 # GEMINI_API_KEY configuration
│   ├── data/                    # CSVs loaded strictly as Data Source files
│   ├── ingest/
│   │   └── loader.py            # The Ingestion logic converting CSVs → Endee vectors
│   ├── website/                 # All Frontend Static Files (HTML/CSS/JS)
│   └── requirements.txt         # Python dependencies
├── docker-compose.yml           # Pre-configured Endee service allocation
└── README.md                    # This document
```

---

## 7. Setup & Installation Instructions

### Prerequisites
- **Python 3.10+**  
- **Docker Desktop** (Required to spin up Endee. Linux/MacOS users may optionally install natively).
- **Google Gemini API Key** ([Free from Google AI Studio](https://aistudio.google.com/app/apikey)).

### Step 1: Clone the Repository
```bash
# Clone your forked repo containing the Endee evaluation
git clone https://github.com/ashokkumarboya93/endee.git
cd endee
```

### Step 2: Start the Endee Vector Database
```bash
# This brings up the Endee vector database container on localhost:8080
docker compose up -d
```

### Step 3: Configure the Python Environment
```bash
# Navigate to the application root
cd debugbot

# Setup a clean Virtual Environment
python -m venv venv

# Activate Environment (Windows)
.\venv\Scripts\activate
# Activate Environment (Linux/MacOS)
source venv/bin/activate

# Install the necessary pip packages
pip install -r requirements.txt
```

### Step 4: Inject the LLM Credentials
Create a `.env` file within the `debugbot/api/` folder:
```env
GEMINI_API_KEY=AIzaSy_your_actual_key_here
```

### Step 5: Data Ingestion (Vectorizing to Endee)
```bash
# Upload all error models from /data directly to the Endee Docker instance
python -m ingest.loader
```
*Expected Output: "Upserting 723 total items into Endee... Data ingestion complete!"*

---

## 8. Running the Application

Execute the FastAPI Application interface:
```bash
cd debugbot
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

The system is fully accessible at:
- **Landing Page/App:** [http://localhost:8000](http://localhost:8000)
- **Debug Interface:** [http://localhost:8000/debug](http://localhost:8000/debug)
- **API Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 9. How It Works — The RAG Pipeline

1. **Text Embedding:** Incoming tracebacks are embedded into a dimensional float array locally.
2. **Vector Query:** This vector goes out to Endee via the python SDK (`client.query()`), searching against an index named `debugbot_errors`. 
3. **Retrieval Selection:** Nearest vectors mathematically representing similar failure paths are recovered, paired with their metadata solutions.
4. **LLM Generation:** The context and the exact traceback are streamed as context to Gemini. The LLM bridges gaps returning pure, structured JSON.
5. **Report Display:** The web app unpackages the JSON and highlights relevant code segments.

---

## 10. Debug Report Structure

Each structured RAG response features:
* **Root Cause:** Deep multi-paragraph breakdown of why code mathematically failed.
* **Solution:** Step-by-step structural fix instructions.
* **Code Examples:** Segmented display comparing the "Wrong Code" with the "Fixed Code".
* **Semantic Matches:** Explicit raw matches straight from the Endee DB showing the user how similar we matched to a historical issue.
* **Reference Links:** Automatically inferred links directly to official Documentation/StackOverflow matching the intent of the bug.

---

## 11. API Endpoints

### `POST /search`
**Goal:** Query the Endee Index
**Payload:** `{"error_string": "IndexError", "language": "python", "top_k": 3}`

### `POST /rag`
**Goal:** Run context against Gemini Flash 2.0.
**Payload:** `{"error_string": "...", "language": "python", "retrieved_contexts": [...]}`

---

## 12. Data Ingestion

The ingestion process reads raw CSV tables holding hundreds of software bugs. 
It utilizes the native `endee` Python package effectively:
```python
client = Endee()
index = client.get_index(name="debugbot_errors")
# Creates representations and upserts directly over HTTP 
embeddings = model.encode(errors, convert_to_numpy=True)
index.upsert(vectors) 
```

---

## 13. Example Queries

* **Python Query:** `IndexError: list index out of range` → Automatically catches boundaries out of context.
* **MongoDB Query:** `Duplicate Key Error: Ensure unique index fields` → Finds write conflict thresholds.
* **JavaScript Query:** `TypeError: Cannot read properties of undefined (reading 'map')` → Analyzes Optional chaining patterns gracefully using RAG.

---

## 14. Use of Endee (Why Endee?)

Pursuant to the **Endee Hiring Evaluation**, the core Vector capability fully leverages **Endee Vector Database** exclusively. 

**Why was Endee optimal for Errorlens AI?**
1. **Performance at Edge:** Leveraging Endee’s C++ core with HNSW structuring provides the exact sub-millisecond responses needed when performing real-time programmatic debugging.
2. **Simpler Python Integration:** The Endee Python SDK provides a highly intuitive operational structure mapping tightly to PyTorch matrices without clunky boilerplate.
3. **Containerized Agility:** Endee spun up flawlessly inside the provided `docker-compose.yml`, reducing complexity allowing us to strictly focus on the RAG interface.
4. **Accurate Cosine Processing:** Evaluates strict dimensional similarities effortlessly directly fitting the error-code mapping threshold requirements perfectly.

---

## 15. Acknowledgements

We extend our heartfelt gratitude to the **Endee** team for providing this robust vector database architecture and evaluation framework. The Endee Vector Database serves reliably as the backbone of Errorlens AI's semantic search capabilities.

This project wouldn't exist without the vision and technology that Endee brings to the AI ecosystem. Thank you for empowering developers to build smarter applications.

---

<p align="center">
  <strong>Errorlens AI</strong> &copy; 2026 — Built by Ashok Kumar Boya<br>
  Designed for the Endee.io Hiring Evaluation Pipeline
</p>

<p align="center">
  <img height="100" alt="Endee" src="./docs/assets/logo-dark.svg">
</p>

# Errorlens AI — Semantic Debug Report Generator

**An intelligent, RAG-powered debugging assistant that understands your errors semantically and generates structured, actionable debug reports.**

> Built with **Endee Vector Database** · **Google Gemini AI** · **Sentence Transformers** · **FastAPI**

---

## Table of Contents

1. [Overview](#1-overview)
2. [Key Features](#2-key-features)
3. [System Architecture](#3-system-architecture)
4. [Technology Stack](#4-technology-stack)
5. [Supported Languages & Databases](#5-supported-languages--databases)
6. [Project Structure](#6-project-structure)
7. [Setup & Installation](#7-setup--installation)
8. [Running the Application](#8-running-the-application)
9. [How It Works — The RAG Pipeline](#9-how-it-works--the-rag-pipeline)
10. [Debug Report Structure](#10-debug-report-structure)
11. [API Endpoints](#11-api-endpoints)
12. [Frontend Pages](#12-frontend-pages)
13. [Data Ingestion](#13-data-ingestion)
14. [Example Queries](#14-example-queries)
15. [Why Endee?](#15-why-endee)
16. [Future Improvements](#16-future-improvements)
17. [Acknowledgements](#17-acknowledgements)

---

## 1. Overview

**Errorlens AI** is a full-stack AI debugging assistant that goes far beyond simple keyword matching. When a developer pastes an error message, stack trace, or describes an issue, Errorlens AI:

1. **Embeds** the error text into a 384-dimensional semantic vector using Sentence Transformers
2. **Searches** the Endee Vector Database for the most similar known error patterns using cosine similarity
3. **Generates** a comprehensive, structured debug report using Google Gemini AI (RAG) or an intelligent fallback system
4. **Presents** the report in a beautiful, exportable format with code examples, reference links, and prevention tips

The application supports **8 languages and databases**: Python, Java, JavaScript, MySQL, MongoDB, Redis, Firebase, and Cassandra — with **700+ curated error patterns** in the vector database.

---

## 2. Key Features

### Semantic Search (NLP)
- **Meaning-based matching** — finds errors based on semantic similarity, not keyword overlap
- *"object is null"* correctly matches *"NullPointerException"* even though zero words overlap
- Powered by `all-MiniLM-L6-v2` producing 384-dimensional embeddings
- Sub-second retrieval via Endee's HNSW indexing algorithm

### RAG Report Generation (LLM)
- **Structured debug reports** with root cause, description, solution, code examples, and prevention tips
- **Language-specific code samples** — both erroneous and corrected code for Python, Java, JS, MySQL, MongoDB, Redis, Firebase, Cassandra
- **Reference links** — auto-generated documentation URLs (docs.python.org, dev.mysql.com, redis.io, etc.)
- **Keyword highlighting** — important terms are extracted and highlighted throughout the report
- **Graceful fallback** — when Gemini quota is exhausted, a rich fallback generator produces equally detailed reports

### Modern Web UI
- **Landing page** — professional toon-flat design with animated sections explaining Semantic Search, RAG concepts, architecture, and supported technologies
- **Debug console** — centered input with language selector, example cards, and loading animation
- **Report page** — multi-section cards with colored stripes, code tabs (Error Code / Fixed Code), visual explanations, semantic match scores, and reference links
- **Developer page** — profile section with social links (LinkedIn, GitHub, Portfolio)
- **Export options** — JSON, TXT download, and Copy to Clipboard with toast notifications
- **Thank You Endee** footer acknowledging Endee's contribution

### Multi-Language Support
| Language | Error Patterns | Type |
|----------|:-----------:|------|
| Python | 200+ | Programming Language |
| Java | 180+ | Programming Language |
| JavaScript | 250+ | Programming Language |
| MySQL | 42 | Relational Database |
| MongoDB | 21 | NoSQL Database |
| Redis | 10 | In-Memory Store |
| Firebase | 10 | Cloud Platform |
| Cassandra | 5 | Distributed Database |

---

## 3. System Architecture

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

### Data Flow

```
User Input (Error String)
    │
    ▼
┌─ Phase 1: Semantic Search ───────────────────┐
│  1. Encode error → 384-dim vector            │
│  2. Query Endee with cosine similarity       │
│  3. Return Top-K similar error patterns      │
└──────────────────────────────────────────────┘
    │
    ▼
┌─ Phase 2: RAG Report Generation ─────────────┐
│  4. Build context from retrieved errors       │
│  5. Send context + query to Gemini AI         │
│  6. Parse structured JSON response            │
│  7. If Gemini unavailable → fallback report   │
│  8. Add code samples + reference links        │
└──────────────────────────────────────────────┘
    │
    ▼
Structured Debug Report (JSON → Rendered HTML)
```

---

## 4. Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Vector Database** | Endee (C++ HNSW Engine) | High-performance semantic similarity search |
| **Backend API** | FastAPI (Python) | REST endpoints for search, RAG, and static file serving |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 | Converts text → 384-dimensional vectors |
| **LLM** | Google Gemini 2.0 Flash | Generates structured debug reports via RAG |
| **Frontend** | HTML + CSS + Vanilla JavaScript | No framework — pure, fast, custom UI |
| **Fonts** | Plus Jakarta Sans + JetBrains Mono | Professional typography from Google Fonts |
| **Containerization** | Docker Compose | Runs Endee vector database locally |
| **Data Format** | CSV → Endee Vectors | Curated error-solution-language-context datasets |

---

## 5. Supported Languages & Databases

### Programming Languages
- **Python** — IndexError, KeyError, TypeError, AttributeError, ValueError, ImportError, NameError, ZeroDivisionError, FileNotFoundError, and 200+ more
- **Java** — NullPointerException, ArrayIndexOutOfBoundsException, ClassCastException, StackOverflowError, ConcurrentModificationException, and 180+ more
- **JavaScript** — TypeError, ReferenceError, SyntaxError, RangeError, async/await errors, Promise rejections, and 250+ more

### Database Technologies
- **MySQL** — Deadlocks, syntax errors, duplicate entries, foreign key violations, connection issues, lock timeouts, and 42 total patterns
- **MongoDB** — Duplicate key errors, write conflicts, cursor timeouts, aggregation pipeline errors, schema validation, and 21 total patterns
- **Redis** — Connection refused, WRONGTYPE errors, memory limits, persistence failures, cluster issues, and 10 total patterns
- **Firebase** — Permission denied, validation errors, quota exceeded, auth failures, data conflicts, and 10 total patterns
- **Cassandra** — Key conflicts, unavailable exceptions, consistency errors, read/write timeouts, and 5 total patterns

---

## 6. Project Structure

```
endee/
├── debugbot/
│   ├── api/
│   │   ├── main.py              # FastAPI backend (search, RAG, static serving)
│   │   └── .env                 # GEMINI_API_KEY configuration
│   ├── data/
│   │   ├── python_errors.csv    # 200+ Python error patterns
│   │   ├── java_errors.csv      # 180+ Java error patterns
│   │   ├── javascript_errors.csv # 250+ JavaScript error patterns
│   │   └── sql_errors.csv       # 93 database error patterns (MySQL/MongoDB/Redis/Firebase/Cassandra)
│   ├── ingest/
│   │   └── loader.py            # Vectorizes CSVs → Endee vector database
│   ├── website/
│   │   ├── index.html           # Landing page (concepts, RAG pipeline, features, architecture)
│   │   ├── landing.css          # Landing page styles (toon-flat professional theme)
│   │   ├── debug.html           # Debug console (input, report, developer page)
│   │   ├── debug.css            # Debug console styles (bright theme, report cards)
│   │   ├── debug.js             # Frontend logic (search, report rendering, exports)
│   │   ├── report.html          # Legacy report page
│   │   ├── app.js               # Legacy application script
│   │   └── styles.css           # Legacy styles
│   ├── requirements.txt         # Python dependencies
│   └── venv/                    # Virtual environment
├── docker-compose.yml           # Docker configuration for Endee
├── errorlens.md                 # This file — comprehensive documentation
└── README.md                    # Original README
```

---

## 7. Setup & Installation

### Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.10+ | Backend runtime |
| Docker Desktop | Latest | Runs Endee Vector Database |
| Google Gemini API Key | Free tier | RAG report generation |

### Step 1: Clone the Repository

```bash
git clone https://github.com/ashokkumarboya93/endee.git
cd endee
```

### Step 2: Start Endee Vector Database

```bash
docker compose up -d
```

This starts the Endee server on port `8080`. Verify it's running:

```bash
docker ps
# Should show endee container running
```

### Step 3: Create Python Virtual Environment

```bash
cd debugbot

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install fastapi uvicorn sentence-transformers endee google-generativeai pandas python-dotenv requests pydantic
```

### Step 5: Configure Google Gemini API Key

Create a `.env` file in `debugbot/api/`:

```env
GEMINI_API_KEY=AIzaSy_your_actual_key_here
```

Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Step 6: Ingest Error Data into Vector Database

```bash
python -m ingest.loader
```

This processes all 4 CSV files (Python, Java, JavaScript, SQL/NoSQL), encodes them into 384-dimensional vectors, and upserts them into the Endee index `debugbot_errors`.

Expected output:

```
Loading embedding model...
Connecting to Endee Vector Database...
Processing python_errors.csv...
  Computing embeddings for 200 errors...
Processing java_errors.csv...
  Computing embeddings for 180 errors...
Processing javascript_errors.csv...
  Computing embeddings for 250 errors...
Processing sql_errors.csv...
  Computing embeddings for 93 errors...
Upserting 723 total items into Endee...
Data ingestion complete!
```

---

## 8. Running the Application

Start the FastAPI server:

```bash
cd debugbot
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

The application is now accessible at:

| Page | URL | Description |
|------|-----|-------------|
| Landing Page | http://localhost:8000 | Hero, concepts, RAG pipeline, features, architecture, supported languages |
| Debug Console | http://localhost:8000/debug | Error input, report generation, developer profile |
| API Docs | http://localhost:8000/docs | Swagger/OpenAPI auto-generated documentation |

---

## 9. How It Works — The RAG Pipeline

### Phase 1: Semantic Search

When a user submits an error string:

1. **Text Embedding** — The error is encoded using `all-MiniLM-L6-v2` into a 384-dimensional float vector
2. **Vector Query** — The vector is sent to Endee's `.query()` method with cosine similarity
3. **Language Filter** — If a specific language is selected, results are filtered by language metadata
4. **Top-K Retrieval** — The top-K most similar error patterns are returned with their solutions, contexts, and similarity scores

### Phase 2: Report Generation

The retrieved contexts are sent to the RAG endpoint:

1. **Context Building** — Retrieved error-solution pairs are formatted into a structured prompt
2. **Gemini Generation** — Google Gemini 2.0 Flash processes the context + original query and generates a structured JSON report
3. **Fallback System** — If Gemini is unavailable (quota exhausted), a detailed fallback generator creates the report using:
   - Multi-paragraph root cause analysis
   - Language-specific code samples (error vs. fixed)
   - Auto-generated reference documentation links
   - Keyword extraction for highlighting
   - Prevention tips and visual explanations
4. **Report Enrichment** — Code samples, reference links, and highlighted keywords are added

### Fallback Intelligence

The fallback system generates rich reports even without Gemini:

- **Python errors** → Python-specific code with `try/except`, list bounds checking, dict `.get()` patterns
- **Java errors** → Java code with null checks, `Optional<>`, arrays `.length` validation
- **JavaScript errors** → JS code with optional chaining `?.`, `Array.isArray()`, `typeof` guards
- **MySQL errors** → SQL queries with `FOR UPDATE`, `ON DUPLICATE KEY UPDATE`, transaction retry logic
- **MongoDB errors** → MongoDB shell commands with `updateOne()`, `upsert`, `findOne()` patterns
- **Redis errors** → Python redis client with `ConnectionError` handling, type checking
- **Firebase errors** → Firebase SDK with `onAuthStateChanged`, security rules, path validation
- **Cassandra errors** → CQL with `IF NOT EXISTS`, consistency levels, retry strategies

---

## 10. Debug Report Structure

Every generated report contains these sections:

| Section | Card Style | Content |
|---------|-----------|---------|
| **Report Banner** | Gradient header | Logo, error title, language badge, confidence score |
| **Summary** | Green border | One-line overview of the error |
| **Root Cause** | Red stripe | Multi-paragraph analysis of why the error occurs |
| **Description** | Blue stripe | Detailed explanation of the error mechanism |
| **Solution** | Green stripe | Step-by-step fix instructions |
| **Code Examples** | Tabbed card | "Error Code" and "Fixed Code" tabs with language syntax |
| **Visual Explanation** | Purple stripe | Flow diagram of error → cause → fix |
| **Prevention Tips** | Amber card | Numbered tips with amber circle badges |
| **Semantic Matches** | Card grid | Top-K similar errors with similarity scores and solutions |
| **Reference Links** | Link grid | External documentation, Stack Overflow, tutorials |
| **Export Section** | Bottom bar | JSON export, TXT download, Copy to Clipboard |
| **Thank You Footer** | Gradient card | Acknowledgement to Endee |

---

## 11. API Endpoints

### `POST /search` — Semantic Error Search

Embeds the error string and queries the Endee vector database.

**Request:**
```json
{
  "error_string": "IndexError: list index out of range",
  "language": "python",
  "top_k": 5
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "python_42",
      "score": 0.954,
      "error": "IndexError: list index out of range",
      "solution": "Check list length before accessing index...",
      "language": "Python",
      "context": "Occurs when accessing an index beyond list boundaries."
    }
  ]
}
```

### `POST /rag` — RAG Report Generation

Takes retrieved contexts and generates an AI report.

**Request:**
```json
{
  "error_string": "IndexError: list index out of range",
  "language": "python",
  "retrieved_contexts": [ ... ]
}
```

**Response:**
```json
{
  "source": "gemini",
  "report": {
    "error_title": "IndexError: list index out of range",
    "language": "python",
    "confidence_score": 95,
    "summary": "...",
    "root_cause": "Multi-paragraph analysis...",
    "description": "Detailed explanation...",
    "solution": "Step-by-step fix...",
    "example_code": "# Wrong code...",
    "fixed_code": "# Corrected code...",
    "visual_explanation": "Error Flow → ...",
    "prevention_tips": ["Tip 1", "Tip 2", ...],
    "references": [...],
    "reference_links": [
      {"title": "Python Docs — Exceptions", "url": "https://docs.python.org/..."}
    ],
    "highlighted_keywords": ["IndexError", "list", "index"]
  }
}
```

### `GET /` — Landing Page

Serves the Errorlens AI landing page with concepts, features, and architecture.

### `GET /debug` — Debug Console

Serves the debug console with input, report rendering, and developer profile.

---

## 12. Frontend Pages

### Landing Page (`/`)
- **Hero Section** — Animated gradient background, "Debugging, Now With Superpowers" headline, stats bar (726+ patterns, 8 languages, <2s report time)
- **Concepts Section** — Visual explanation of Semantic Search vs. Keyword Search, and RAG pipeline flow
- **RAG Pipeline** — 6-step pipeline cards (Input → Embed → Search → Retrieve → Generate → Report)
- **Features** — 6 feature cards (Vector Search, RAG Reports, Multi-Language, Structured Output, Fallback AI, Export)
- **Architecture** — Dark-themed system architecture diagram
- **Futuristic Section** — Future capabilities (real-time learning, multi-modal, CI/CD integration)
- **Power Section** — Why Errorlens stands out (context-aware, sub-second, structured, resilient)
- **Thank You Endee** — Gratitude section with technology logos
- **Supported Languages** — 8-card grid showing all supported languages with error counts
- **CTA** — "Launch Errorlens AI" call-to-action

### Debug Console (`/debug`)
- **Input Page** — Centered input with bug icon, textarea, language selector (8 options), results selector, 6 example cards (Python, Java, JS, MySQL, MongoDB, Redis)
- **Report Page** — Sticky topbar with export buttons, DebugBot Report banner, multi-section card layout, footer
- **Developer Page** — Profile card with avatar, bio, social links (LinkedIn, GitHub, Portfolio)
- **Loading Overlay** — 3-step animation (Embedding → Searching → Generating)

---

## 13. Data Ingestion

### CSV Format

All datasets follow this schema:

```csv
error,solution,language,context
"IndexError: list index out of range","Check list length before accessing...","Python","Occurs when accessing beyond boundaries."
```

### Dataset Files

| File | Records | Languages |
|------|:-------:|-----------|
| `python_errors.csv` | 200+ | Python |
| `java_errors.csv` | 180+ | Java |
| `javascript_errors.csv` | 250+ | JavaScript |
| `sql_errors.csv` | 93 | MySQL (42), MongoDB (21), Redis (10), Firebase (10), Cassandra (5) |

### Ingestion Process (`ingest/loader.py`)

```python
# 1. Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Connect to Endee
client = Endee()
index = client.get_index(name="debugbot_errors")

# 3. For each CSV: encode errors → create vectors → upsert to Endee
embeddings = model.encode(errors, convert_to_numpy=True)
index.upsert(vectors)  # Batched in chunks of 300
```

---

## 14. Example Queries

### Python — IndexError
**Input:** `IndexError: list index out of range`
**Language:** Python
**Result:** Report with list bounds checking, `len()` validation, try/except patterns

### Java — NullPointerException
**Input:** `NullPointerException: Cannot invoke method on null object`
**Language:** Java
**Result:** Report with null checks, `Optional<>`, defensive coding patterns

### JavaScript — TypeError
**Input:** `TypeError: Cannot read properties of undefined (reading 'map')`
**Language:** JavaScript
**Result:** Report with optional chaining `?.`, `Array.isArray()`, nullish coalescing

### MySQL — Deadlock
**Input:** `Deadlock Detected: Transactions blocking each other`
**Language:** MySQL
**Result:** Report with consistent lock ordering, `FOR UPDATE`, transaction retry logic

### MongoDB — Duplicate Key
**Input:** `Duplicate Key Error: Ensure unique index fields`
**Language:** MongoDB
**Result:** Report with `updateOne()` upsert, uniqueness checks, `findOne()` guards

### Redis — Connection Refused
**Input:** `Connection Refused: Redis server not running`
**Language:** Redis
**Result:** Report with connection pooling, `ping()` health checks, timeout configuration

---

## 15. Why Endee?

Endee was chosen as the vector database for Errorlens AI because:

1. **Performance** — Built in C++ with native AVX2/NEON/SVE2 optimizations for blazing-fast vector operations
2. **HNSW Indexing** — Hierarchical Navigable Small World algorithm for approximate nearest neighbor search at scale
3. **Simple Python SDK** — `pip install endee` provides a clean, intuitive API
4. **Docker Support** — Single `docker compose up -d` to start the server
5. **Cosine Similarity** — Native support for cosine distance, ideal for semantic text embeddings
6. **INT8 Precision** — Reduced memory footprint while maintaining search accuracy
7. **Production Ready** — Handles 700+ vectors with sub-millisecond query latency

---

## 16. Future Improvements

- **Continuous Learning** — Auto-ingest new error patterns from user queries and feedback
- **Hybrid Search** — Combine dense vector search with sparse keyword matching (BM25) supported by Endee
- **Multi-Modal Input** — Accept screenshots of error messages and parse them using OCR
- **CI/CD Integration** — GitHub Actions / GitLab CI plugin to auto-debug build failures
- **Live Error Monitoring** — Real-time error stream analysis from application logs
- **User Authentication** — Personal error history and saved reports
- **Custom Datasets** — Allow users to upload their own error-solution CSVs
- **Dark Mode** — Full dark theme support across all pages

---

## 17. Acknowledgements

We extend our heartfelt gratitude to the **Endee** team for providing this incredible opportunity. The Endee Vector Database is the backbone of Errorlens AI's semantic search capabilities — its high-performance C-based architecture, HNSW indexing, and elegant Python SDK made it possible to build a production-grade RAG system with remarkable speed and reliability.

This project wouldn't exist without the vision and technology that Endee brings to the vector database ecosystem. Thank you for empowering developers to build smarter, faster, and more intelligent applications.

### Technologies & Credits

| Technology | Role |
|-----------|------|
| [Endee Vector Database](https://github.com/endee-io/endee) | Semantic vector search engine |
| [Google Gemini AI](https://ai.google.dev) | LLM for RAG report generation |
| [Sentence Transformers](https://www.sbert.net) | Text embedding model (all-MiniLM-L6-v2) |
| [FastAPI](https://fastapi.tiangolo.com) | Backend REST API framework |
| [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) | Primary typeface |
| [JetBrains Mono](https://www.jetbrains.com/lp/mono/) | Code typography |

---

<p align="center">
  <strong>Errorlens AI</strong> &copy; 2026 — Built by Ashok Kumar Boya<br>
  Semantic AI Debugging &middot; RAG Pipeline &middot; Vector Search
</p>

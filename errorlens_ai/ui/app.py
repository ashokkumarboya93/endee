import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="DebugBot.ai — AI Debugging Assistant",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────  BRIGHT MODERN THEME  ─────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
        color: #1e293b;
    }

    /* ── Page Background ── */
    .stApp {
        background: linear-gradient(160deg, #f0f4ff 0%, #e0e7ff 40%, #faf5ff 100%);
    }

    /* ── Hero Banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        padding: 2.5rem 2rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.35);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 60%);
        animation: shimmer 8s ease-in-out infinite;
    }
    @keyframes shimmer {
        0%, 100% { transform: translate(0, 0); }
        50% { transform: translate(30%, 30%); }
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        position: relative;
        text-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .hero-sub {
        color: rgba(255,255,255,0.85);
        font-size: 1.05rem;
        font-weight: 400;
        margin-top: 0.4rem;
        position: relative;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #4f46e5 !important;
    }

    /* ── Input Area ── */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 2px solid #c7d2fe !important;
        border-radius: 16px !important;
        font-family: 'JetBrains Mono', 'Consolas', monospace !important;
        font-size: 0.9rem !important;
        padding: 1rem !important;
        transition: border-color 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }

    /* ── Primary Button ── */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        padding: 0.85rem 2rem !important;
        border-radius: 14px !important;
        letter-spacing: 0.05em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── Result Cards ── */
    .result-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: all 0.35s ease;
    }
    .result-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.12);
        border-color: #c7d2fe;
    }
    .result-card .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
    }
    .result-card .card-title {
        font-weight: 700;
        font-size: 1.05rem;
        color: #1e293b;
    }
    .match-pill {
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        font-family: monospace;
    }
    .match-high { background: #dcfce7; color: #15803d; }
    .match-mid  { background: #fef9c3; color: #a16207; }
    .match-low  { background: #fee2e2; color: #b91c1c; }

    .lang-badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 9999px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .lang-python     { background: #dbeafe; color: #1d4ed8; }
    .lang-java       { background: #ffedd5; color: #c2410c; }
    .lang-javascript { background: #fef3c7; color: #92400e; }

    .context-block {
        background: #f8fafc;
        padding: 0.9rem 1rem;
        border-radius: 10px;
        margin-top: 0.8rem;
        color: #475569;
        font-size: 0.92rem;
        line-height: 1.6;
        border-left: 4px solid #6366f1;
    }
    .fix-block {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 0.9rem 1rem;
        border-radius: 10px;
        margin-top: 0.6rem;
        border: 1px solid #a7f3d0;
    }
    .fix-block b { color: #059669; }
    .fix-block span { color: #064e3b; display: block; margin-top: 0.3rem; }

    /* ── AI Card ── */
    .ai-card {
        background: linear-gradient(145deg, #eef2ff 0%, #e0e7ff 100%);
        padding: 1.8rem;
        border-radius: 18px;
        border: 1px solid #c7d2fe;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.1);
        color: #1e293b;
        line-height: 1.7;
        font-size: 0.95rem;
    }
    .ai-card h1, .ai-card h2, .ai-card h3 {
        color: #4f46e5;
    }
    .ai-card code {
        background: #c7d2fe;
        padding: 2px 6px;
        border-radius: 4px;
        color: #3730a3;
    }
    .ai-card strong { color: #312e81; }
    .ai-card ul, .ai-card ol { padding-left: 1.5rem; }

    /* ── Status Panel ── */
    .status-panel {
        background: #ffffff;
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }
    .status-panel h4 { color: #4f46e5; margin-top: 0; }
    .status-dot {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    .dot-green { background: #22c55e; }
    .dot-yellow { background: #eab308; }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* ── Section Headers ── */
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Footer ── */
    .footer-bar {
        text-align: center;
        padding: 1.5rem;
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────  HERO  ──────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🐛 DebugBot.ai</div>
    <div class="hero-sub">Semantic Search + RAG AI  •  Powered by Endee Vector Database & Google Gemini</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────  SIDEBAR  ──────────────────────────────────
with st.sidebar:
    st.markdown("### 🎯 Configuration")
    language = st.selectbox("Language / Ecosystem", ["Python", "JavaScript", "Java", "All"], index=0)
    top_k = st.slider("Results to Retrieve (Top-K)", min_value=1, max_value=10, value=3)

    st.divider()
    st.markdown("### 🧠 AI Engine")
    use_rag = st.toggle("Enable Gemini RAG", value=True,
                        help="Uses retrieved context + Google Gemini to generate a custom explanation.")

    st.divider()
    st.markdown("""
    💡 **Tips for best results:**
    - Paste the **full traceback**, not just the error line.
    - Select the correct language for filtered results.
    - Use Top-K ≥ 3 for more context in RAG mode.
    """)

# ──────────────────────────────────  MAIN AREA  ──────────────────────────────────
col_main, col_status = st.columns([2.5, 1])

with col_main:
    query = st.text_area(
        "🔎 Paste your error message or stacktrace",
        height=180,
        placeholder="Traceback (most recent call last):\n  File \"app.py\", line 42, in <module>\n    result = data[index]\nIndexError: list index out of range"
    )
    search_clicked = st.button("🚀 Diagnose Error")

with col_status:
    st.markdown("""
    <div class="status-panel">
        <h4>📡 System Health</h4>
        <p><span class="status-dot dot-green"></span> <strong>Endee DB</strong> — Connected</p>
        <p><span class="status-dot dot-green"></span> <strong>Embedding Model</strong> — Loaded</p>
        <p><span class="status-dot dot-green"></span> <strong>Gemini Flash</strong> — Ready</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="status-panel" style="margin-top:1rem;">
        <h4>📖 How It Works</h4>
        <ol style="padding-left:1.2rem; color:#475569; font-size:0.9rem;">
            <li><strong>Encode</strong> — Your error → 384-dim vector</li>
            <li><strong>Search</strong> — Cosine similarity in Endee</li>
            <li><strong>Explain</strong> — Gemini generates a tailored fix</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────  SEARCH + DISPLAY  ──────────────────────────────────
if search_clicked:
    if not query.strip():
        st.toast("Please paste an error message first!", icon="⚠️")
    else:
        # ── Step 1: NLP Semantic Search ──
        with st.spinner("🔍 Searching the semantic knowledge base..."):
            try:
                res = requests.post(f"{API_URL}/search", json={
                    "error_string": query,
                    "language": language,
                    "top_k": top_k
                }, timeout=15)
                res.raise_for_status()
                nlp_results = res.json().get("results", [])
            except requests.exceptions.ConnectionError:
                st.error("⚡ Cannot reach the backend API. Make sure FastAPI is running on port 8000.")
                nlp_results = []
            except Exception as e:
                st.error(f"Backend error: {e}")
                nlp_results = []

        if not nlp_results:
            st.warning("No similar errors found. Try rephrasing or pasting the full traceback.")
        else:
            st.divider()

            col_hits, col_ai = st.columns([1, 1.3])

            # ── Left: Semantic Hits ──
            with col_hits:
                st.markdown('<div class="section-header">🗂️ Semantic Matches</div>', unsafe_allow_html=True)

                for r in nlp_results:
                    score = float(r.get('score', 0))
                    pct = score * 100
                    match_cls = "match-high" if score > 0.8 else "match-mid" if score > 0.6 else "match-low"
                    lang_val = r.get('language', 'Python')
                    lang_cls = f"lang-{lang_val.lower()}"

                    st.markdown(f"""
                    <div class="result-card">
                        <div class="card-header">
                            <span class="card-title">📌 Matched Pattern</span>
                            <span class="match-pill {match_cls}">{pct:.1f}% match</span>
                        </div>
                        <span class="lang-badge {lang_cls}">{lang_val}</span>
                        <div class="context-block">
                            <strong>Error:</strong> {r.get('error', 'N/A')}<br/>
                            <strong>Context:</strong> {r.get('context', 'N/A')}
                        </div>
                        <div class="fix-block">
                            <b>✅ Recommended Fix:</b>
                            <span>{r.get('solution', 'N/A')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── Right: AI Explanation ──
            with col_ai:
                if use_rag:
                    st.markdown('<div class="section-header">🤖 AI-Powered Explanation</div>', unsafe_allow_html=True)
                    with st.spinner("🧠 Generating intelligent analysis with Gemini..."):
                        try:
                            rag_res = requests.post(f"{API_URL}/rag", json={
                                "error_string": query,
                                "language": language,
                                "retrieved_contexts": nlp_results
                            }, timeout=30)

                            if rag_res.status_code == 403:
                                st.warning("🔑 Gemini API key not configured on the server. RAG is unavailable.")
                            elif rag_res.status_code != 200:
                                st.error(f"RAG endpoint returned {rag_res.status_code}: {rag_res.text}")
                            else:
                                explanation = rag_res.json().get("explanation", "")
                                st.markdown(f'<div class="ai-card">{explanation}</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"RAG request failed: {e}")
                else:
                    st.info("💡 Toggle **Enable Gemini RAG** in the sidebar for AI-powered explanations.")

# ── Footer ──
st.markdown("""
<div class="footer-bar">
    Built with ❤️ using <strong>Endee Vector Database</strong>, <strong>Sentence Transformers</strong>, and <strong>Google Gemini</strong>
</div>
""", unsafe_allow_html=True)

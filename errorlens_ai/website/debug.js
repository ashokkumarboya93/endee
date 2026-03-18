/* ═══════════════════════════════════════════════════
   Errorlens AI Debug Console — Enhanced Report with Exports
   ═══════════════════════════════════════════════════ */
const API = '';
let currentReport = null;

const inputPage = document.getElementById('inputPage');
const reportPage = document.getElementById('reportPage');
const reportContent = document.getElementById('reportContent');
const reportQuery = document.getElementById('reportQuery');
const errorInput = document.getElementById('errorInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const langSelect = document.getElementById('langSelect');
const topKSelect = document.getElementById('topKSelect');
const backBtn = document.getElementById('backBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const loadingText = document.getElementById('loadingText');

backBtn.addEventListener('click', () => {
  reportPage.style.display = 'none';
  inputPage.style.display = 'flex';
  window.scrollTo(0, 0);
});
analyzeBtn.addEventListener('click', handleSubmit);
errorInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSubmit(); }
});
document.querySelectorAll('.example-card').forEach(card => {
  card.addEventListener('click', () => {
    errorInput.value = card.dataset.error;
    langSelect.value = card.dataset.lang;
    handleSubmit();
  });
});

async function handleSubmit() {
  const errorStr = errorInput.value.trim();
  if (!errorStr) return;
  const lang = langSelect.value;
  const topK = parseInt(topKSelect.value);
  analyzeBtn.disabled = true;
  showLoading(true);
  setStep(1);
  try {
    const searchRes = await fetch(`${API}/search`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error_string: errorStr, language: lang, top_k: topK })
    });
    if (!searchRes.ok) throw new Error(`Search failed (${searchRes.status})`);
    const searchData = await searchRes.json();
    const results = searchData.results || [];
    setStep(2);
    const ragRes = await fetch(`${API}/rag`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error_string: errorStr, language: lang, retrieved_contexts: results })
    });
    if (!ragRes.ok) throw new Error(`RAG failed (${ragRes.status})`);
    const ragData = await ragRes.json();
    setStep(3);
    currentReport = ragData.report;
    currentReport._source = ragData.source;
    currentReport._query = errorStr;
    setTimeout(() => {
      showLoading(false);
      inputPage.style.display = 'none';
      reportPage.style.display = 'block';
      reportQuery.textContent = errorStr;
      renderReport(currentReport);
      window.scrollTo(0, 0);
    }, 400);
  } catch (err) {
    showLoading(false);
    inputPage.style.display = 'none';
    reportPage.style.display = 'block';
    reportQuery.textContent = errorStr;
    reportContent.innerHTML = `<div class="error-card"><h3>Analysis Failed</h3><p>${esc(err.message)}. Please ensure backend & Docker/Endee are running.</p></div>`;
  }
  analyzeBtn.disabled = false;
}
function showLoading(show) { loadingOverlay.style.display = show ? 'flex' : 'none'; }
function setStep(n) {
  ['ls1', 'ls2', 'ls3'].forEach((id, i) => {
    document.getElementById(id).className = 'lstep' + (i + 1 < n ? ' done' : (i + 1 === n ? ' active' : ''));
  });
  loadingText.textContent = ['Embedding error message...', 'Searching vector database...', 'Generating AI report...'][n - 1] || 'Processing...';
}

/* ═══ HIGHLIGHT KEYWORDS ═══ */
function highlightText(text, keywords) {
  if (!text || !keywords || !keywords.length) return esc(text);
  let result = esc(text);
  keywords.forEach(kw => {
    const escaped = kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    result = result.replace(new RegExp(`(${escaped})`, 'gi'), '<mark class="hl">$1</mark>');
  });
  return result;
}

/* ═══ LANG HELPERS ═══ */
function langLabel(l) {
  const map = { python: 'Python', java: 'Java', javascript: 'JavaScript', mysql: 'MySQL', mongodb: 'MongoDB', redis: 'Redis', firebase: 'Firebase', cassandra: 'Cassandra', sql: 'SQL', all: 'Code' };
  return map[(l || '').toLowerCase()] || l || 'Code';
}
function langClass(l) {
  const map = { python: 'lang-py', java: 'lang-java', javascript: 'lang-js', mysql: 'lang-sql', mongodb: 'lang-mongo', redis: 'lang-redis', firebase: 'lang-firebase', cassandra: 'lang-cassandra' };
  return map[(l || '').toLowerCase()] || 'lang-default';
}

/* ═══ FORMAT MULTILINE TEXT ═══ */
function formatParagraph(text, kw) {
  if (!text) return '';
  // Split on newlines and numbered steps
  const lines = text.split('\n').filter(l => l.trim());
  if (lines.length <= 1) return `<p>${highlightText(text, kw)}</p>`;
  let html = '';
  let inList = false;
  lines.forEach(line => {
    const trimmed = line.trim();
    if (/^\d+[\.\)]/.test(trimmed)) {
      if (!inList) { html += '<ol class="rcard-ol">'; inList = true; }
      html += `<li>${highlightText(trimmed.replace(/^\d+[\.\)]\s*/, ''), kw)}</li>`;
    } else {
      if (inList) { html += '</ol>'; inList = false; }
      html += `<p>${highlightText(trimmed, kw)}</p>`;
    }
  });
  if (inList) html += '</ol>';
  return html;
}

/* ═══ RENDER REPORT ═══ */
function renderReport(r) {
  const kw = r.highlighted_keywords || [];
  const conf = (r.confidence_score || '').toLowerCase();
  const confClass = conf === 'high' ? 'badge-high' : conf === 'medium' ? 'badge-medium' : 'badge-low';
  const lang = langLabel(r.language);
  const lc = langClass(r.language);

  let h = `<div class="report-block">`;

  // ── REPORT TITLE BANNER ──
  h += `<div class="report-banner">
    <div class="rb-logo">
      <svg viewBox="0 0 40 36" width="36" height="32" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="1" width="30" height="24" rx="3" fill="rgba(255,255,255,0.15)"/><circle cx="5" cy="5" r="1" fill="rgba(255,255,255,0.4)" stroke="none"/><circle cx="9" cy="5" r="1" fill="rgba(255,255,255,0.4)" stroke="none"/><circle cx="13" cy="5" r="1" fill="rgba(255,255,255,0.4)" stroke="none"/><line x1="1" y1="9" x2="31" y2="9" stroke="rgba(255,255,255,0.2)"/><polyline points="10 15 6 19 10 23"/><polyline points="22 15 26 19 22 23"/><line x1="18" y1="14" x2="14" y2="24"/><circle cx="31" cy="25" r="8" fill="rgba(255,255,255,0.15)"/><circle cx="31" cy="24" r="3" fill="none"/></svg>
    </div>
    <div class="rb-text">
      <div class="rb-label">Errorlens AI Report</div>
      <h1 class="rb-title">${esc(r.error_title || 'Debug Analysis Report')}</h1>
    </div>
    <div class="rb-badges">
      <span class="badge badge-lang">${esc(lang)}</span>
      <span class="badge ${confClass}">${esc(r.confidence_score || 'N/A')}</span>
      <span class="badge badge-ai">${r._source === 'gemini' ? 'AI Generated' : 'Semantic Match'}</span>
    </div>
  </div>`;

  // ── SUMMARY ──
  if (r.summary) {
    h += `<div class="summary-banner"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00B894" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> <strong>Summary:</strong> ${highlightText(r.summary, kw)}</div>`;
  }

  // ── ROOT CAUSE ──
  if (r.root_cause) {
    h += `<div class="rcard rcard-pill rcard-red">
      <div class="rcard-stripe stripe-red"></div>
      <div class="rcard-body">
        <div class="rcard-head"><div class="rcard-icon ic-red"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#E74C3C" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><path d="M12 9v4M12 17h.01"/></svg></div><div><div class="rcard-label">Root Cause</div><div class="rcard-title">Why This Error Occurs</div></div></div>
        ${formatParagraph(r.root_cause, kw)}
      </div>
    </div>`;
  }

  // ── DESCRIPTION ──
  if (r.description) {
    h += `<div class="rcard rcard-wide">
      <div class="rcard-stripe stripe-blue"></div>
      <div class="rcard-body">
        <div class="rcard-head"><div class="rcard-icon ic-blue"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0984E3" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg></div><div><div class="rcard-label">Analysis</div><div class="rcard-title">Technical Description</div></div></div>
        ${formatParagraph(r.description, kw)}
      </div>
    </div>`;
  }

  // ── SOLUTION ──
  if (r.solution) {
    h += `<div class="rcard rcard-featured">
      <div class="rcard-stripe stripe-green"></div>
      <div class="rcard-body">
        <div class="rcard-head"><div class="rcard-icon ic-green"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00B894" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg></div><div><div class="rcard-label">Solution</div><div class="rcard-title">How to Fix It</div></div></div>
        ${formatParagraph(r.solution, kw)}
      </div>
    </div>`;
  }

  // ── CODE: ERROR vs FIXED ──
  if (r.example_code || r.fixed_code) {
    h += `<div class="rcard rcard-code-card">
      <div class="rcard-head"><div class="rcard-icon ic-violet"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6C5CE7" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg></div><div><div class="rcard-label">${esc(lang)} Code</div><div class="rcard-title">Error Code vs Fixed Code</div></div></div>
      <div class="code-tabs">
        <button class="code-tab tab-wrong active" onclick="switchTab(this,'wrong')"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6M9 9l6 6"/></svg> Error Code</button>
        <button class="code-tab tab-fixed" onclick="switchTab(this,'fixed')"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg> Fixed Code</button>
      </div>
      <div class="code-panel active" id="panel-wrong"><div class="code-block ${lc}"><div class="code-lang-tag">${esc(lang)}</div>${esc(r.example_code || '// No example available')}</div></div>
      <div class="code-panel" id="panel-fixed"><div class="code-block ${lc}"><div class="code-lang-tag">${esc(lang)}</div>${esc(r.fixed_code || '// No fix available')}</div></div>
    </div>`;
  }

  // ── VISUAL EXPLANATION ──
  if (r.visual_explanation) {
    h += `<div class="rcard rcard-visual">
      <div class="rcard-head"><div class="rcard-icon ic-cyan"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00CEC9" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg></div><div><div class="rcard-label">Visual</div><div class="rcard-title">Error Flow Diagram</div></div></div>
      <div class="visual-box">${esc(r.visual_explanation)}</div>
    </div>`;
  }

  // ── PREVENTION TIPS ──
  if (r.prevention_tips && r.prevention_tips.length) {
    h += `<div class="rcard rcard-tips">
      <div class="rcard-head"><div class="rcard-icon ic-amber"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#D4A017" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div><div><div class="rcard-label">Prevention</div><div class="rcard-title">Best Practices to Avoid This Error</div></div></div>
      <ul class="tips-list">${r.prevention_tips.map((t, i) => `<li><span class="tip-num">${i + 1}</span>${highlightText(t, kw)}</li>`).join('')}</ul>
    </div>`;
  }

  // ── SEMANTIC MATCHES FROM ENDEE ──
  if (r.references && r.references.length) {
    h += `<div class="rcard rcard-matches">
      <div class="rcard-head"><div class="rcard-icon ic-orange"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#E17055" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0018 0V5"/><path d="M3 12a9 3 0 0018 0"/></svg></div><div><div class="rcard-label">Endee Database</div><div class="rcard-title">Semantic Matches</div></div></div>
      <div class="ref-grid">${r.references.map((ref, i) => `
        <div class="ref-item">
          <div class="ref-head"><span class="ref-num">#${i + 1}</span>${ref.score ? `<span class="ref-score">${(ref.score * 100).toFixed(1)}%</span>` : ''}</div>
          <p class="ref-error">${esc((ref.error || '').substring(0, 160))}</p>
          <p class="ref-fix">${esc((ref.solution || '').substring(0, 160))}</p>
        </div>`).join('')}
      </div>
    </div>`;
  }

  // ── REFERENCE LINKS (at the end) ──
  if (r.reference_links && r.reference_links.length) {
    h += `<div class="rcard rcard-links">
      <div class="rcard-head"><div class="rcard-icon ic-blue"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0984E3" stroke-width="2"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg></div><div><div class="rcard-label">References</div><div class="rcard-title">Documentation & Resources</div></div></div>
      <div class="links-grid">${r.reference_links.map(link => `
        <a href="${esc(link.url)}" target="_blank" rel="noopener" class="link-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          <div><strong>${esc(link.title)}</strong><span>${esc(link.url)}</span></div>
        </a>`).join('')}
      </div>
    </div>`;
  }

  // ── EXPORT OPTIONS AT BOTTOM ──
  h += `<div class="report-export-bottom">
    <div class="reb-label">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><path d="M12 15V3"/></svg>
      Export this report
    </div>
    <div class="reb-buttons">
      <button class="reb-btn reb-json" onclick="exportJSON()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6"/></svg>
        Export JSON
      </button>
      <button class="reb-btn reb-download" onclick="downloadReport()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><path d="M12 15V3"/></svg>
        Download .txt
      </button>
      <button class="reb-btn reb-copy" onclick="copyReport()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
        Copy to Clipboard
      </button>
    </div>
  </div>`;

  h += `</div>`;
  reportContent.innerHTML = h;
}

/* ═══ HELPERS ═══ */
function esc(s) { if (!s) return ''; const d = document.createElement('div'); d.textContent = String(s); return d.innerHTML }
function switchTab(btn, panel) {
  btn.closest('.rcard').querySelectorAll('.code-tab').forEach(t => t.classList.remove('active'));
  btn.closest('.rcard').querySelectorAll('.code-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('panel-' + panel).classList.add('active');
}

/* ═══ EXPORTS ═══ */
function getClean() {
  if (!currentReport) return null;
  const { _source, _query, ...c } = currentReport;
  return { error_title: c.error_title || '', language: c.language || '', confidence_score: c.confidence_score || '', root_cause: c.root_cause || '', description: c.description || '', solution: c.solution || '', example_code: c.example_code || '', fixed_code: c.fixed_code || '', visual_explanation: c.visual_explanation || '', prevention_tips: c.prevention_tips || [], summary: c.summary || '', highlighted_keywords: c.highlighted_keywords || [], reference_links: c.reference_links || [], references: (c.references || []).map(r => ({ error: r.error, solution: r.solution, language: r.language, score: r.score })) };
}
function exportJSON() {
  const d = getClean(); if (!d) return;
  const b = new Blob([JSON.stringify(d, null, 2)], { type: 'application/json' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = `errorlens_report_${Date.now()}.json`; a.click();
  showExportToast('JSON exported!');
}
function downloadReport() {
  const d = getClean(); if (!d) return;
  let t = `╔══════════════════════════════════════════════════════╗\n║            DEBUGBOT.AI — DEBUG REPORT                ║\n╚══════════════════════════════════════════════════════╝\n\nError: ${d.error_title}\nLanguage: ${d.language}\nConfidence: ${d.confidence_score}\n\n${'─'.repeat(54)}\nROOT CAUSE\n${'─'.repeat(54)}\n${d.root_cause}\n\n${'─'.repeat(54)}\nDESCRIPTION\n${'─'.repeat(54)}\n${d.description}\n\n${'─'.repeat(54)}\nSOLUTION\n${'─'.repeat(54)}\n${d.solution}\n\n${'─'.repeat(54)}\nERROR CODE (${d.language})\n${'─'.repeat(54)}\n${d.example_code}\n\n${'─'.repeat(54)}\nFIXED CODE (${d.language})\n${'─'.repeat(54)}\n${d.fixed_code}\n\n${'─'.repeat(54)}\nVISUAL EXPLANATION\n${'─'.repeat(54)}\n${d.visual_explanation}\n\n${'─'.repeat(54)}\nPREVENTION TIPS\n${'─'.repeat(54)}\n${(d.prevention_tips || []).map((t, i) => `${i + 1}. ${t}`).join('\n')}\n\n${'─'.repeat(54)}\nREFERENCE LINKS\n${'─'.repeat(54)}\n${(d.reference_links || []).map(l => `• ${l.title}\n  ${l.url}`).join('\n')}\n\nSUMMARY: ${d.summary}\n\n— Generated by Errorlens AI\n`;
  const b = new Blob([t], { type: 'text/plain' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = `errorlens_report_${Date.now()}.txt`; a.click();
  showExportToast('Report downloaded!');
}
function copyReport() {
  const d = getClean(); if (!d) return;
  navigator.clipboard.writeText(JSON.stringify(d, null, 2)).then(() => showExportToast('Copied to clipboard!'));
}
function showExportToast(msg) {
  let t = document.getElementById('exportToast');
  if (!t) { t = document.createElement('div'); t.id = 'exportToast'; t.className = 'export-toast'; document.body.appendChild(t) }
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}

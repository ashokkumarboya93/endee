/* ══════════════════════════════════════════════════
   Errorlens AI — Debug Console Application Logic
   ══════════════════════════════════════════════════ */

const API = window.location.origin;
let currentReport = null;

/* ═══ SVG Icon Helpers ═══ */
const ICONS = {
  arrowLeft: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>',
  bug: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m8 2 1.88 1.88"/><path d="M14.12 3.88 16 2"/><path d="M9 7.13v-1a3.003 3.003 0 1 1 6 0v1"/><path d="M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6"/><path d="M12 20v-9"/><path d="M6.53 9C4.6 8.8 3 7.1 3 5"/><path d="M6 13H2"/><path d="M3 21c0-2.1 1.7-3.9 3.8-4"/><path d="M20.97 5c0 2.1-1.6 3.8-3.5 4"/><path d="M22 13h-4"/><path d="M17.2 17c2.1.1 3.8 1.9 3.8 4"/></svg>',
  search: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
  brain: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a8 8 0 0 0-8 8c0 6 8 12 8 12s8-6 8-12a8 8 0 0 0-8-8Z"/><circle cx="12" cy="10" r="3"/></svg>',
  check: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="m9 12 2 2 4-4"/></svg>',
  lightbulb: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>',
  link: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" x2="21" y1="14" y2="3"/></svg>',
  file: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/></svg>',
  database: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/></svg>',
  arrowRight: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>',
  clipboard: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/></svg>',
  shield: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
  flow: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
};

/* ═══ SIDEBAR & NAVIGATION ═══ */

function toggleSidebar() {
  const sb = document.getElementById('sidebar');
  sb.classList.toggle('collapsed');
  const icon = document.getElementById('collapseIcon');
  if (sb.classList.contains('collapsed')) {
    icon.innerHTML = '<polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/>';
  } else {
    icon.innerHTML = '<polyline points="11 17 6 12 11 7"/><polyline points="18 17 13 12 18 7"/>';
  }
}

function showPage(page) {
  ['home', 'reports', 'about'].forEach(p => {
    document.getElementById(`page-${p}`).style.display = 'none';
    document.getElementById(`nav-${p}`).classList.remove('active');
  });
  document.getElementById(`page-${page}`).style.display = 'block';
  document.getElementById(`nav-${page}`).classList.add('active');
  const titles = { home: 'Home', reports: 'Reports', about: 'About' };
  document.getElementById('pageTitle').textContent = titles[page];
}

/* ═══ EXAMPLE CHIPS ═══ */

function useExample(text) {
  document.getElementById('errorInput').value = text;
  document.getElementById('errorInput').focus();
}

/* ═══ LOADING ═══ */

function showLoading() {
  document.getElementById('loadingOverlay').classList.add('active');
  for (let i = 1; i <= 4; i++) {
    const el = document.getElementById(`ls${i}`);
    el.classList.remove('active', 'done');
    el.querySelector('.step-check svg').style.display = 'none';
  }
  document.getElementById('ls1').classList.add('active');
}

function advanceStep(n) {
  for (let i = 1; i < n; i++) {
    const el = document.getElementById(`ls${i}`);
    el.classList.remove('active');
    el.classList.add('done');
    el.querySelector('.step-check svg').style.display = 'block';
  }
  const cur = document.getElementById(`ls${n}`);
  if (cur) cur.classList.add('active');
}

function hideLoading() {
  for (let i = 1; i <= 4; i++) {
    const el = document.getElementById(`ls${i}`);
    el.classList.remove('active');
    el.classList.add('done');
    el.querySelector('.step-check svg').style.display = 'block';
  }
  setTimeout(() => document.getElementById('loadingOverlay').classList.remove('active'), 500);
}

/* ═══ GENERATE REPORT ═══ */

async function generateReport() {
  const errorText = document.getElementById('errorInput').value.trim();
  const language = document.getElementById('languageSelect').value;
  const topK = parseInt(document.getElementById('topkSelect').value);

  if (!errorText) {
    const ta = document.getElementById('errorInput');
    ta.style.animation = 'shake 0.4s ease';
    ta.style.borderColor = 'var(--red-500)';
    setTimeout(() => { ta.style.animation = ''; ta.style.borderColor = ''; }, 1500);
    return;
  }

  document.getElementById('submitBtn').disabled = true;
  showLoading();

  try {
    advanceStep(1);
    await sleep(500);

    // Search
    advanceStep(2);
    const searchRes = await fetch(`${API}/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error_string: errorText, language, top_k: topK })
    });

    if (!searchRes.ok) {
      const err = await searchRes.json().catch(() => ({}));
      throw new Error(err.detail || `Search failed (${searchRes.status})`);
    }

    const searchData = await searchRes.json();
    const results = searchData.results || [];

    // RAG
    advanceStep(3);
    let aiExplanation = null;

    if (results.length > 0) {
      try {
        const ragRes = await fetch(`${API}/rag`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ error_string: errorText, language, retrieved_contexts: results })
        });
        if (ragRes.ok) {
          const ragData = await ragRes.json();
          aiExplanation = ragData.explanation;
        }
      } catch (e) { console.warn('RAG unavailable:', e); }
    }

    // Build Report
    advanceStep(4);
    await sleep(300);

    currentReport = { errorText, language, results, aiExplanation, timestamp: new Date() };
    renderReport(currentReport);
    hideLoading();
    setTimeout(() => showPage('reports'), 250);

  } catch (err) {
    hideLoading();
    showToast(err.message);
  } finally {
    document.getElementById('submitBtn').disabled = false;
  }
}

/* ═══ RENDER REPORT ═══ */

function renderReport(rpt) {
  const container = document.getElementById('reportContainer');
  const errorShort = extractErrorName(rpt.errorText);
  const ts = rpt.timestamp.toLocaleString();
  const mc = rpt.results.length;

  let h = '';

  // Header
  h += `
    <div class="report-header">
      <a class="back-link" onclick="showPage('home')">${ICONS.arrowLeft} New Report</a>
      <div class="report-meta-row">
        <span class="meta-badge lang">${esc(rpt.language)}</span>
        <span class="meta-badge time">${ts}</span>
        <span class="meta-badge count">${mc} match${mc !== 1 ? 'es' : ''}</span>
      </div>
      <h1 class="report-title">Debug Report: ${esc(errorShort)}</h1>
      <div class="error-display">${esc(rpt.errorText)}</div>
    </div>
  `;

  // Flow Diagram
  h += `
    <div class="flow-diagram" style="animation: slideUp 0.3s var(--ease) both;">
      <h3>${ICONS.flow} Error Resolution Flow</h3>
      <div class="flow-row">
        <div class="flow-node">
          <div class="flow-node-icon">${ICONS.bug}</div>
          <div class="flow-node-title">Error Detected</div>
          <div class="flow-node-sub">${esc(errorShort)}</div>
        </div>
        <div class="flow-connector">${ICONS.arrowRight}</div>
        <div class="flow-node">
          <div class="flow-node-icon">${ICONS.search}</div>
          <div class="flow-node-title">Semantic Search</div>
          <div class="flow-node-sub">${mc} patterns found</div>
        </div>
        <div class="flow-connector">${ICONS.arrowRight}</div>
        <div class="flow-node">
          <div class="flow-node-icon">${ICONS.brain}</div>
          <div class="flow-node-title">AI Analysis</div>
          <div class="flow-node-sub">${rpt.aiExplanation ? 'Gemini RAG' : 'DB Fallback'}</div>
        </div>
        <div class="flow-connector">${ICONS.arrowRight}</div>
        <div class="flow-node highlight">
          <div class="flow-node-icon">${ICONS.check}</div>
          <div class="flow-node-title">Solution Ready</div>
          <div class="flow-node-sub">Report generated</div>
        </div>
      </div>
    </div>
  `;

  // Similarity Matches
  if (mc > 0) {
    h += `
      <div class="report-section" style="animation: slideUp 0.4s var(--ease) 0.1s both;">
        <div class="section-head">
          <h3>${ICONS.database} Semantic Similarity Matches</h3>
          <span class="section-tag">${mc} found</span>
        </div>
        <div class="section-content">
          <div class="match-list">
    `;
    rpt.results.forEach((r, i) => {
      const pct = Math.round((r.score || 0) * 100);
      const color = pct >= 70 ? 'var(--green-500)' : pct >= 40 ? 'var(--amber-500)' : 'var(--red-500)';
      h += `
        <div class="match-item" style="animation: slideUp 0.3s var(--ease) ${0.05 * i}s both;">
          <div class="match-top">
            <div class="match-name">${esc(r.error || 'Unknown Error')}</div>
            <div class="match-score-wrap">
              <div class="score-track"><div class="score-bar" style="width:${pct}%;background:${color};"></div></div>
              <span class="score-num" style="color:${color};">${pct}%</span>
            </div>
          </div>
          <span class="match-lang-tag">${r.language || 'Unknown'}</span>
          <div class="match-context">${esc(r.context || 'No context available.')}</div>
          <div class="match-fix">
            ${ICONS.lightbulb}
            <p>${esc(r.solution || 'No solution available.')}</p>
          </div>
        </div>
      `;
    });
    h += `</div></div></div>`;
  }

  // AI Section
  h += `
    <div class="report-section" style="animation: slideUp 0.4s var(--ease) 0.2s both;">
      <div class="section-head">
        <h3>${ICONS.brain} AI-Powered Debug Analysis</h3>
        <span class="section-tag">${rpt.aiExplanation ? 'Gemini RAG' : 'Fallback'}</span>
      </div>
      <div class="ai-body">
        ${rpt.aiExplanation ? rpt.aiExplanation : buildFallback(rpt)}
      </div>
    </div>
  `;

  // Summary
  if (mc > 0) {
    h += `
      <div class="summary-banner" style="animation: slideUp 0.4s var(--ease) 0.3s both;">
        <h3>${ICONS.clipboard} Quick Summary</h3>
        <p>${esc(rpt.results[0].solution || 'Review the error context and apply the suggested fix.')}</p>
      </div>
    `;
  }

  // Reference Links
  h += buildRefLinks(rpt);

  container.innerHTML = h;
}

/* ═══ FALLBACK ═══ */

function buildFallback(rpt) {
  if (!rpt.results.length) return '<p>No matches found. Try a different error or select "All Languages".</p>';
  const t = rpt.results[0];
  let h = `
    <div class="rag-section">
      <h3>What This Error Means</h3>
      <p>${esc(t.context || 'This error occurs during runtime execution.')}</p>
    </div>
    <div class="rag-section">
      <h3>How To Fix It</h3>
      <p><strong>Recommended:</strong> ${esc(t.solution || 'Review the error context.')}</p>
  `;
  if (rpt.results.length > 1) {
    h += '<p><strong>Alternative approaches:</strong></p><ul>';
    rpt.results.slice(1).forEach(r => { h += `<li>${esc(r.solution || '')}</li>`; });
    h += '</ul>';
  }
  h += `</div>
    <div class="rag-section">
      <h3>Prevention Tips</h3>
      <ul>
        <li>Always validate inputs and check boundary conditions.</li>
        <li>Use proper exception handling (try/catch/except).</li>
        <li>Write unit tests that cover edge cases.</li>
      </ul>
    </div>
  `;
  return h;
}

/* ═══ REFERENCE LINKS ═══ */

function buildRefLinks(rpt) {
  const lang = rpt.language.toLowerCase();
  const q = encodeURIComponent(rpt.errorText.substring(0, 80));
  const links = [];

  if (lang === 'python' || lang === 'all')
    links.push({ label: 'Python Documentation', url: 'https://docs.python.org/3/' });
  if (lang === 'java' || lang === 'all')
    links.push({ label: 'Java SE Docs', url: 'https://docs.oracle.com/en/java/' });
  if (lang === 'javascript' || lang === 'all')
    links.push({ label: 'MDN Web Docs', url: 'https://developer.mozilla.org/' });

  links.push({ label: 'Search StackOverflow', url: `https://stackoverflow.com/search?q=${q}` });
  links.push({ label: 'Google this error', url: `https://www.google.com/search?q=${q}` });
  links.push({ label: 'Endee Documentation', url: 'https://endee.io' });

  let h = `
    <div class="report-section" style="animation: slideUp 0.4s var(--ease) 0.4s both;">
      <div class="section-head">
        <h3>${ICONS.link} Reference Links</h3>
      </div>
      <div class="section-content">
        <div class="ref-grid">
  `;

  links.forEach(l => {
    h += `<a class="ref-item" href="${l.url}" target="_blank" rel="noopener">${ICONS.link}<span>${l.label}</span></a>`;
  });

  return h + '</div></div></div>';
}

/* ═══ UTILITIES ═══ */

function extractErrorName(text) {
  const m = text.match(/([A-Z]\w*(?:Error|Exception|Warning|Fault))\s*[:]/i);
  if (m) return m[0];
  return text.length > 55 ? text.substring(0, 55) + '...' : text;
}

function esc(t) {
  const d = document.createElement('div');
  d.textContent = t;
  return d.innerHTML;
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function showToast(msg) {
  let t = document.getElementById('toast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'toast';
    t.style.cssText = 'position:fixed;bottom:28px;right:28px;z-index:9999;background:#fff;border:1px solid var(--red-500);border-radius:var(--r-md);padding:14px 22px;color:var(--red-500);font-size:14px;font-weight:500;box-shadow:var(--shadow-lg);max-width:380px;animation:slideUp 0.3s var(--ease);';
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.style.display = 'block';
  setTimeout(() => { t.style.display = 'none'; }, 5000);
}

// Keyboard shortcut: Ctrl+Enter
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') generateReport();
});

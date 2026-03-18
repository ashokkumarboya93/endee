"""
DebugBot RAG Pipeline — Generator Module
Uses Google Gemini to synthesize a structured debug report from retrieved contexts.
"""

import os
import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class Generator:
    """Sends retrieved context + user error to Gemini for a structured debug report."""

    MODEL_NAME = "gemini-2.0-flash"

    def __init__(self, api_key: str = None):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError(
                "[Generator] GEMINI_API_KEY not found. "
                "Set it in your .env file or pass it directly."
            )
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel(self.MODEL_NAME)
        print(f"[Generator] Gemini model '{self.MODEL_NAME}' configured.")

    def generate(
        self,
        error_string: str,
        language: str,
        retrieved_contexts: List[Dict],
    ) -> str:
        """
        Generate a structured HTML debug report.

        Args:
            error_string: The user's original error message.
            language: The programming language of the error.
            retrieved_contexts: List of dicts from Retriever with keys:
                                error, solution, context, language.

        Returns:
            An HTML string with the structured debug report.
        """
        # Build the context block from retrieved results
        context_str = ""
        for i, ctx in enumerate(retrieved_contexts):
            context_str += f"\n--- Known Error {i + 1} ---\n"
            context_str += f"Similar Error: {ctx.get('error')}\n"
            context_str += f"Context: {ctx.get('context')}\n"
            context_str += f"Solution: {ctx.get('solution')}\n"

        prompt = f"""You are a highly intelligent Senior Software Engineering debugging assistant.
The user has encountered the following {language} error:

USER ERROR: "{error_string}"

Below are some similar known errors retrieved from our semantic database:
{context_str}

Based on the retrieved database errors and your deep technical knowledge, provide a STRUCTURED debug report in clean HTML.

You MUST structure your response with these EXACT section divs:

<div class="rag-section rag-explanation">
<h3>💡 What This Error Means</h3>
<p>Clear explanation of what the error fundamentally is.</p>
</div>

<div class="rag-section rag-cause">
<h3>⚠️ Why It Occurs</h3>
<p>Detailed explanation of the root cause with bullet points if needed.</p>
</div>

<div class="rag-section rag-fix">
<h3>🛠 How To Fix It</h3>
<p>Step-by-step solution with code examples.</p>
</div>

<div class="rag-section rag-code">
<h3>📝 Code Example</h3>
<div class="code-comparison">
<div class="code-block code-before">
<h4>❌ Before (Error)</h4>
<pre><code>Show the buggy code here</code></pre>
</div>
<div class="code-block code-after">
<h4>✅ After (Fixed)</h4>
<pre><code>Show the corrected code here</code></pre>
</div>
</div>
</div>

<div class="rag-section rag-prevention">
<h3>🛡️ Prevention Tips</h3>
<ul><li>Tips to prevent this error in the future.</li></ul>
</div>

<div class="rag-section rag-summary">
<h3>📋 Summary</h3>
<p>One-line summary of the fix.</p>
</div>

Use ONLY HTML tags (h3, h4, p, pre, code, ul, li, div, strong, em). Do NOT use markdown. Keep code examples in {language}."""

        response = self.model.generate_content(prompt)
        return response.text

"""
DebugBot RAG Pipeline — Orchestrator
Ties Embedder → Retriever → Generator into a single run() call.
"""

from typing import Dict
from .embedder import Embedder
from .retriever import Retriever
from .generator import Generator


class DebugBotRAG:
    """
    End-to-end RAG pipeline for DebugBot.ai.

    Flow:
        Error Input → Embedding Model → Endee Vector DB
        → Top-K Retrieval → LLM (Reason + Refine) → Final Structured Output
    """

    def __init__(self, gemini_api_key: str = None):
        print("[DebugBotRAG] Initializing pipeline...")
        self.embedder = Embedder()
        self.retriever = Retriever()
        self.generator = Generator(api_key=gemini_api_key)
        print("[DebugBotRAG] Pipeline ready.\n")

    def run(
        self,
        error_string: str,
        language: str = "all",
        top_k: int = 5,
    ) -> Dict:
        """
        Execute the full RAG pipeline.

        Args:
            error_string: The runtime error message to debug.
            language: Programming language filter ('python', 'java', 'javascript', 'all').
            top_k: Number of similar errors to retrieve.

        Returns:
            A dict with keys:
                - query: the original error string
                - language: the language filter used
                - retrieved: list of top-k similar errors from Endee
                - report: the LLM-generated HTML debug report
        """
        # Step 1: Embed the error string
        print(f"[Pipeline] Embedding query: \"{error_string[:80]}...\"")
        query_vector = self.embedder.embed(error_string)

        # Step 2: Retrieve similar errors from Endee
        print(f"[Pipeline] Searching Endee (top_k={top_k}, lang={language})...")
        results = self.retriever.search(
            query_vector=query_vector,
            language=language,
            top_k=top_k,
        )
        print(f"[Pipeline] Retrieved {len(results)} results.")

        # Step 3: Generate the debug report via LLM
        print("[Pipeline] Generating debug report via Gemini...")
        report = self.generator.generate(
            error_string=error_string,
            language=language,
            retrieved_contexts=results,
        )
        print("[Pipeline] Report generated successfully.")

        return {
            "query": error_string,
            "language": language,
            "retrieved": results,
            "report": report,
        }

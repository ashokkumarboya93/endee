"""
DebugBot RAG Pipeline — Retriever Module
Queries the Endee vector database for semantically similar errors.
"""

from endee import Endee
from typing import List, Dict, Optional


# Map user-facing language names to the canonical DB values
LANGUAGE_MAP = {
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
}


class Retriever:
    """Handles all vector similarity search operations against Endee."""

    INDEX_NAME = "debugbot_errors"

    def __init__(self, endee_client: Optional[Endee] = None):
        self.client = endee_client or Endee()
        self.index = self.client.get_index(self.INDEX_NAME)
        print(f"[Retriever] Connected to Endee index: '{self.INDEX_NAME}'")

    def search(
        self,
        query_vector: List[float],
        language: str = "all",
        top_k: int = 5,
    ) -> List[Dict]:
        """
        Search the vector database for the most similar error signatures.

        Args:
            query_vector: The 384-dim embedding of the user's error string.
            language: Filter results by language ('python', 'java', 'javascript', or 'all').
            top_k: Number of results to return.

        Returns:
            A list of dicts, each with keys: id, score, error, solution, context, language.
        """
        # Build optional language filter
        query_filter = None
        if language.lower() != "all":
            db_lang = LANGUAGE_MAP.get(language.lower(), language)
            query_filter = [{"language": {"$eq": db_lang}}]

        raw_results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            filter=query_filter,
        )

        results = []
        for res in raw_results:
            meta = res.get("meta", {}) if isinstance(res, dict) else {}
            results.append({
                "id": res.get("id", ""),
                "score": res.get("similarity", 0.0),
                "error": meta.get("error", ""),
                "solution": meta.get("solution", ""),
                "context": meta.get("context", ""),
                "language": meta.get("language", ""),
            })

        return results

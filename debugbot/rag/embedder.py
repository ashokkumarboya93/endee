"""
DebugBot RAG Pipeline — Embedder Module
Converts error strings into 384-dimensional vectors using SentenceTransformer.
"""

from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class Embedder:
    """Handles all text-to-vector embedding operations."""

    MODEL_NAME = "all-MiniLM-L6-v2"
    DIMENSION = 384

    def __init__(self):
        print(f"[Embedder] Loading model: {self.MODEL_NAME}...")
        self.model = SentenceTransformer(self.MODEL_NAME)
        print(f"[Embedder] Model loaded. Output dimension: {self.DIMENSION}")

    def embed(self, text: str) -> List[float]:
        """Embed a single text string into a vector."""
        vector = self.model.encode([text], convert_to_numpy=True)[0]
        return vector.tolist()

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Embed a batch of text strings into vectors."""
        return self.model.encode(texts, convert_to_numpy=True)

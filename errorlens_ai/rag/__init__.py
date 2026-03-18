"""
DebugBot RAG Pipeline Package
==============================
Semantic error retrieval and LLM-powered debug report generation.

Usage:
    from rag.pipeline import DebugBotRAG

    pipeline = DebugBotRAG()
    result = pipeline.run(
        error_string="TypeError: 'NoneType' object is not subscriptable",
        language="python",
        top_k=5,
    )
    print(result["report"])
"""

from .pipeline import DebugBotRAG
from .embedder import Embedder
from .retriever import Retriever
from .generator import Generator

__all__ = ["DebugBotRAG", "Embedder", "Retriever", "Generator"]

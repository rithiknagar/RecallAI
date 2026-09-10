from dataclasses import dataclass
from typing import Any
from uuid import UUID
from app.citations.models import Citation


@dataclass
class RetrievedChunk:
    chunk_id: int
    document_id: UUID
    content: str
    # score: float
    metadata: dict[str, Any]
    retrieval_score: float
    rerank_score: float | None = None

@dataclass
class RAGResponse:
    answer: str
    retrieved_chunks: list[RetrievedChunk]
    citations: list[Citation]
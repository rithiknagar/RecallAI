from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass
class RetrievedChunk:
    chunk_id: UUID
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
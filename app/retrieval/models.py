from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass
class RetrievedChunk:
    chunk_id: UUID
    document_id: UUID
    content: str
    score: float
    metadata: dict[str, Any]
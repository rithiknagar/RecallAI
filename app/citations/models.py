from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Citation:
    source_id: str
    document_id: UUID
    chunk_id: int
    source: str | None = None
    page: int | None = None
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from langchain_core.documents import Document


@dataclass
class RetrievalResult:
    document: Document
    score: float

class VectorStore(ABC):

    @abstractmethod
    def add_documents(
        self,
        documents: List[Document],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def similarity_search(
        self,
        query: str,
        k: int,
        metadata_filter: dict[str, object] | None = None,
    ) -> List[RetrievalResult]:
        raise NotImplementedError
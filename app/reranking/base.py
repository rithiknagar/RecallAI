from abc import ABC, abstractmethod

from app.retrieval.models import RetrievedChunk


class Reranker(ABC):

    @abstractmethod
    def rerank(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        top_k: int,
    ) -> list[RetrievedChunk]:
        raise NotImplementedError
from abc import ABC, abstractmethod

from app.retrieval.models import RetrievedChunk


class Retriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        raise NotImplementedError
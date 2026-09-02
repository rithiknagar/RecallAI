from abc import ABC, abstractmethod

from app.retrieval.models import RetrievedChunk


class ContextAssembler(ABC):

    @abstractmethod
    def assemble(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        raise NotImplementedError
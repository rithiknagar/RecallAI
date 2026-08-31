from abc import ABC, abstractmethod

from app.retrieval.models import RetrievedChunk
from app.conversation.models import Message


class PromptBuilder(ABC):

    @abstractmethod
    def build(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        history: list[Message],
    ) -> str:
        raise NotImplementedError
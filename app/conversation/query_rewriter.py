from abc import ABC, abstractmethod

from app.conversation.models import Message


class QueryRewriter(ABC):

    @abstractmethod
    def rewrite(
        self,
        question: str,
        history: list[Message],
    ) -> str:
        raise NotImplementedError
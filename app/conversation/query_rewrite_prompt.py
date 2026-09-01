from abc import ABC, abstractmethod

from app.conversation.models import Message


class QueryRewritePromptBuilder(ABC):

    @abstractmethod
    def build(
        self,
        question: str,
        history: list[Message],
    ) -> str:
        raise NotImplementedError
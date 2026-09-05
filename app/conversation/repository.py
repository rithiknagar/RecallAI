from abc import ABC, abstractmethod
from uuid import UUID

from app.conversation.models import Message


class ConversationRepository(ABC):

    @abstractmethod
    def create_session(self) -> UUID:
        raise NotImplementedError

    @abstractmethod
    def add_message(
        self,
        session_id: UUID,
        role: str,
        content: str,
    ) -> Message:
        raise NotImplementedError

    @abstractmethod
    def get_messages(
        self,
        session_id: UUID,
    ) -> list[Message]:
        raise NotImplementedError

    @abstractmethod
    def get_session(
        self,
        session_id: UUID,):
        raise NotImplementedError
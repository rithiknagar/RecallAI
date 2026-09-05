from uuid import UUID

from app.conversation.models import Message
from app.conversation.repository import (
    ConversationRepository,
)


class ConversationService:

    def __init__(
        self,
        repository: ConversationRepository,
    ) -> None:
        self._repository = repository

    def create_session(self, user_id: UUID, title: str = "New Conversation",) -> UUID:

        session_id = self._repository.create_session(user_id=user_id,title=title,)

        return session_id

    def add_message(
        self,
        session_id: UUID,
        role: str,
        content: str,
    ) -> Message:

        if role not in {
            "user",
            "assistant",
        }:
            raise ValueError(
                f"Invalid message role: {role}"
            )

        if not content.strip():
            raise ValueError(
                "Message content cannot be empty."
            )
        print(f"add message called for role {role} ")


        return self._repository.add_message(
            session_id=session_id,
            role=role,
            content=content,
        )

    def get_history(
        self,
        session_id: UUID,
    ) -> list[Message]:

        return self._repository.get_messages(
            session_id=session_id,
        )
    
    def get_session(self, session_id: UUID,):
    
            return self._repository.get_session(
                session_id=session_id,
            )
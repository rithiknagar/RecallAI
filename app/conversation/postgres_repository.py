from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.conversation.models import Message
from app.conversation.repository import ConversationRepository
from app.vectorstore.models import (
    ConversationMessageModel,
    ConversationSessionModel,
)


class PostgresConversationRepository(
    ConversationRepository
):

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def create_session(self) -> UUID:

        conversation_session = (
            ConversationSessionModel()
        )

        self._session.add(
            conversation_session
        )

        self._session.flush()

        return conversation_session.id

    def add_message(
        self,
        session_id: UUID,
        role: str,
        content: str,
    ) -> Message:

        message_model = ConversationMessageModel(
            session_id=session_id,
            role=role,
            content=content,
        )

        self._session.add(message_model)

        self._session.flush()

        return Message(
            id=message_model.id,
            session_id=message_model.session_id,
            role=message_model.role,
            content=message_model.content,
            created_at=message_model.created_at,
        )

    def get_messages(
        self,
        session_id: UUID,
    ) -> list[Message]:

        statement = (
            select(ConversationMessageModel)
            .where(
                ConversationMessageModel.session_id
                == session_id
            )
            .order_by(
                ConversationMessageModel.created_at
            )
        )

        rows = (
            self._session
            .execute(statement)
            .scalars()
            .all()
        )

        return [
            Message(
                id=row.id,
                session_id=row.session_id,
                role=row.role,
                content=row.content,
                created_at=row.created_at,
            )
            for row in rows
        ]
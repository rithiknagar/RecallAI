from app.core.database import SessionLocal

from app.conversation.postgres_repository import (
    PostgresConversationRepository,
)

from app.conversation.service import (
    ConversationService,
)


session = SessionLocal()

repository = PostgresConversationRepository(
    session
)

conversation_service = ConversationService(
    repository
)

try:

    session_id = (
        conversation_service
        .create_session()
    )

    print("Session:", session_id)

    conversation_service.add_message(
        session_id=session_id,
        role="user",
        content="How many annual leave days do employees get?",
    )

    conversation_service.add_message(
        session_id=session_id,
        role="assistant",
        content="Employees receive 27 days.",
    )

    conversation_service.add_message(
        session_id=session_id,
        role="user",
        content="Can they carry them forward?",
    )

    history = (
        conversation_service
        .get_history(session_id)
    )

    for message in history:

        print(
            f"[{message.role}] "
            f"{message.content}"
        )

    session.commit()

except Exception:

    session.rollback()

    raise

finally:

    session.close()
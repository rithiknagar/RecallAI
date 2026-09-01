from datetime import datetime
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column

from app.core.database import Base
from app.core.config import settings


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    filename = Column(
        String(500),
        nullable=False,
    )

    title = Column(
        String(500),
        nullable=True,
    )
    content_hash = Column(
        String(64),
        nullable=True,
    )

    document_type = Column(
        String(100),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    chunks = relationship(
        "DocumentChunkModel",
        back_populates="document",
        cascade="all, delete-orphan",
    )


class DocumentChunkModel(Base):
    __tablename__ = "document_chunks"

    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    document_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    chunk_index = Column(
        Integer,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    chunk_metadata = Column(
        "metadata",
        JSON,
        nullable=False,
        default=dict,
    )

    embedding = Column(
        Vector(settings.vector_dimension),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    document = relationship(
        "DocumentModel",
        back_populates="chunks",
    )


class ConversationSessionModel(Base):
    __tablename__ = "conversation_sessions"

    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    messages = relationship(
        "ConversationMessageModel",
        back_populates="session",
        cascade="all, delete-orphan",
    )

class ConversationMessageModel(Base):
    __tablename__ = "conversation_messages"

    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    session_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey(
            "conversation_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    role = Column(
        String(20),
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    session = relationship(
        "ConversationSessionModel",
        back_populates="messages",
    )
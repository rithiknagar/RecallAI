from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Message:
    id: UUID
    session_id: UUID
    role: str
    content: str
    created_at: datetime

@dataclass
class Conversation:
    session_id: UUID
    messages: list[Message]
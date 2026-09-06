from pydantic import BaseModel, Field
from uuid import UUID


class ChatRequest(BaseModel):

    session_id: UUID

    question: str = Field(
        min_length=1,
        max_length=5000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

class CitationResponse(BaseModel):

    source_id: str
    document_id: str
    source: str | None
    page: int | None
    chunk_id: int


class ChatResponse(BaseModel):

    answer: str

class CreateConversation(BaseModel):
    user_id:UUID
    title:str
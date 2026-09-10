from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse, CitationResponse
from app.rag.conversational_service import ConversationalRAGService
from app.core.dependencies import get_rag_service
from app.auth.utils import verify_token
import re

router=APIRouter(prefix="/chat",tags=["chat"])

@router.get("")
def chat():
    return {"message":"chat service"}

@router.post("", response_model=ChatResponse,)
def chat( request: ChatRequest, curr_user=Depends(verify_token), rag_service: ConversationalRAGService = Depends( get_rag_service )):

    session=rag_service._conversation_service.get_session(request.session_id)

    if session.user_id != curr_user.id:
            raise HTTPException(status_code=401,detail="You are unauthorized")
    
    response = rag_service.ask(
        session_id=request.session_id,
        question=request.question,
        top_k=request.top_k,
    )
    print(response.answer)

    # Extract source IDs referenced in the answer
    referenced_source_ids = set(re.findall(r"\[S\d+\]", response.answer))
    
    
    citation_responses = [
        CitationResponse(
            source_id=citation.source_id,
            document_id=citation.document_id,
            chunk_id=citation.chunk_id,
            source=citation.source,
            page=citation.page
        )
        for citation in response.citations
        if f"[{citation.source_id}]" in referenced_source_ids
    ]

    return ChatResponse(answer=response.answer, citations=citation_responses)
        
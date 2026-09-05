from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chat import CreateConversation
from app.rag.conversational_service import ConversationalRAGService
from app.conversation.service import ConversationService
from app.core.dependencies import get_rag_service, get_conversation_service
from uuid import UUID
from app.auth.utils import verify_token




router=APIRouter(prefix="/conversation",tags=["conversations"])

@router.post("")
def create_conversation(request:CreateConversation, conversation_service:ConversationService = Depends( get_conversation_service ) )->UUID:

    session_id=conversation_service.create_session(request.user_id,request.title)

    return session_id

@router.get("/{session_id}")
def create_conversation(session_id:UUID, curr_user=Depends(verify_token), conversation_service:ConversationService = Depends( get_conversation_service ) ):

    session=conversation_service.get_session(session_id)
    
    if session.user_id != curr_user.id:
        raise HTTPException(status_code=401,detail="You are unauthorized")
    
    conversations=conversation_service.get_history(session_id)

    return conversations


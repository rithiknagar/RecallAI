from fastapi import APIRouter
from app.api.v1.chat import router as chat_router
from app.api.v1.conversation import router as conversation_router
from app.api.v1.auth import router as auth_router

router=APIRouter(prefix="/api/v1")

router.include_router(chat_router)
router.include_router(conversation_router)
router.include_router(auth_router)
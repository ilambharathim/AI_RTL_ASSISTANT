"""
FastAPI route for Kiwi Engineering Assistant API endpoint.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from app.ai.kiwi_provider import KiwiAIProviderManager

router = APIRouter()


class KiwiChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class KiwiChatRequest(BaseModel):
    messages: List[KiwiChatMessage]
    project_context: Optional[Dict[str, Any]] = {}


@router.post("/kiwi/chat")
def chat_with_kiwi(payload: KiwiChatRequest):
    """
    POST /api/kiwi/chat
    Executes context-aware chat turn with Kiwi Engineering Assistant.
    """
    provider_mgr = KiwiAIProviderManager()
    msg_dicts = [{"role": m.role, "content": m.content} for m in payload.messages]
    context = payload.project_context or {}

    response = provider_mgr.generate_chat_response(msg_dicts, context)
    return response

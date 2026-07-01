from typing import List, Literal

from pydantic import BaseModel, HttpUrl


# ==========================================================
# Incoming Chat Messages
# ==========================================================

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# ==========================================================
# Recommendation Model
# ==========================================================

class Recommendation(BaseModel):
    name: str
    url: HttpUrl
    test_type: str


# ==========================================================
# Chat Response
# ==========================================================

class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool = False


# ==========================================================
# Health Response
# ==========================================================

class HealthResponse(BaseModel):
    status: str = "ok"
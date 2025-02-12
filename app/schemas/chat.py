from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class ChatMessageType(str):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ChatRequest(BaseModel):
    message: str
    detection_id: Optional[int] = None
    conversation_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ChatResponse(BaseModel):
    message_id: str
    conversation_id: str
    response: str
    model: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    detection_id: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    sources: List[Dict[str, Any]] = Field(default_factory=list)

class Conversation(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)
    messages: List[ChatMessage] = Field(default_factory=list)

class ConversationList(BaseModel):
    conversations: List[Conversation]
    total: int

class AIModelInfo(BaseModel):
    id: str
    name: str
    description: str
    max_tokens: int
    supports_functions: bool
    is_available: bool

class AICapabilities(BaseModel):
    models: List[AIModelInfo]
    features: List[str]
    max_context_length: int
    supports_streaming: bool

class AISuggestion(BaseModel):
    text: str
    confidence: float
    action: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import json
import logging

from datetime import datetime
from sqlalchemy.future import select

from ....db.session import get_db
from ....models.detection import Detection
from ....schemas.chat import (
    ChatRequest, ChatResponse, Conversation, ConversationList,
    AIModelInfo, AICapabilities, AISuggestion, ChatMessage
)
from ....services.ai_analyst import AIAnalyst
from ....websocket.manager import ConnectionManager

router = APIRouter()
logger = logging.getLogger(__name__)
ws_manager = ConnectionManager()

# Initialize AI Analyst
ai_analyst = AIAnalyst()

# In-memory storage for conversations (in a production app, use a database)
conversations: Dict[str, Conversation] = {}

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """Send a message to the AI analyst"""
    try:
        # Get or create conversation
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        if conversation_id not in conversations:
            conversations[conversation_id] = Conversation(
                id=conversation_id,
                title=f"Conversation {conversation_id[:8]}",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                messages=[]
            )
        
        conversation = conversations[conversation_id]
        
        # Add user message to conversation
        user_message = ChatMessage(
            role="user",
            content=request.message,
            metadata=request.metadata or {}
        )
        conversation.messages.append(user_message)
        
        # Get detection context if provided
        detection = None
        if request.detection_id:
            result = await db.execute(
                select(Detection).where(Detection.id == request.detection_id)
            )
            detection = result.scalars().first()
            if not detection:
                raise HTTPException(status_code=404, detail="Detection not found")
        
        # Get AI response
        response = await ai_analyst.chat(
            message=request.message,
            detection_context=detection.dict() if detection else None
        )
        
        # Add assistant response to conversation
        assistant_message = ChatMessage(
            role="assistant",
            content=response["response"],
            metadata={
                "model": response["model"],
                "detection_id": request.detection_id
            }
        )
        conversation.messages.append(assistant_message)
        conversation.updated_at = datetime.utcnow()
        
        # Create response
        return ChatResponse(
            message_id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            response=response["response"],
            model=response["model"],
            detection_id=request.detection_id,
            metadata={
                "conversation_title": conversation.title,
                "message_count": len(conversation.messages)
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations", response_model=ConversationList)
async def list_conversations(
    skip: int = 0,
    limit: int = 20
):
    """List all conversations"""
    conv_list = list(conversations.values())
    return ConversationList(
        conversations=conv_list[skip:skip+limit],
        total=len(conv_list)
    )

@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation by ID"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversations[conversation_id]

@router.delete("/conversations/{conversation_id}", status_code=204)
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id in conversations:
        del conversations[conversation_id]
    return None

@router.get("/models", response_model=AICapabilities)
async def get_ai_capabilities():
    """Get information about available AI models and capabilities"""
    return AICapabilities(
        models=[
            AIModelInfo(
                id="gpt-4",
                name="GPT-4",
                description="Most capable model, better than any GPT-3.5 model, able to do more complex tasks, and optimized for chat.",
                max_tokens=8192,
                supports_functions=True,
                is_available=True
            ),
            AIModelInfo(
                id="gpt-3.5-turbo",
                name="GPT-3.5 Turbo",
                description="Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003.",
                max_tokens=4096,
                supports_functions=False,
                is_available=True
            )
        ],
        features=[
            "chat",
            "detection_analysis",
            "threat_intel",
            "mitre_mapping"
        ],
        max_context_length=8192,
        supports_streaming=True
    )

@router.websocket("/ws/{client_id}")
async def websocket_chat(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time chat"""
    await ws_manager.connect(websocket, client_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                
                if message.get("type") == "message":
                    # Handle chat message
                    request = ChatRequest(**{
                        "message": message.get("content", ""),
                        "conversation_id": message.get("conversation_id"),
                        "detection_id": message.get("detection_id"),
                        "metadata": message.get("metadata", {})
                    })
                    
                    # Process the message
                    response = await chat(request, get_db())
                    
                    # Send response back to client
                    await ws_manager.send_personal_message({
                        "type": "message",
                        "conversation_id": response.conversation_id,
                        "message_id": response.message_id,
                        "content": response.response,
                        "role": "assistant",
                        "timestamp": datetime.utcnow().isoformat(),
                        "metadata": {
                            "model": response.model,
                            "detection_id": response.detection_id
                        }
                    }, client_id)
                
            except json.JSONDecodeError:
                await ws_manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON"
                }, client_id)
                
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await ws_manager.send_personal_message({
            "type": "error",
            "message": str(e)
        }, client_id)
        ws_manager.disconnect(client_id)

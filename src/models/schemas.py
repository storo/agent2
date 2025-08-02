from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ChatRequest(BaseModel):
    """Modelo para requests de chat"""
    message: str = Field(..., description="Mensaje del usuario")
    session_id: Optional[str] = Field(None, description="ID de sesión para continuidad")
    user_id: Optional[str] = Field(None, description="ID del usuario")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Contexto adicional")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Quiero crear una campaña para mi producto",
                "session_id": "session_123",
                "user_id": "user_456",
                "context": {
                    "platform": "web",
                    "language": "es"
                }
            }
        }

class ChatResponse(BaseModel):
    """Modelo para respuestas síncronas de chat"""
    session_id: str
    message_id: str
    content: str
    agent_used: str
    tools_used: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str
    
class StreamChatResponse(BaseModel):
    """Modelo para respuestas de streaming"""
    type: str  # "start", "chunk", "end", "error"
    session_id: Optional[str] = None
    message_id: Optional[str] = None
    content: Optional[str] = None
    agent_used: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str

class AgentStatus(BaseModel):
    """Estado de un agente"""
    name: str
    status: str  # "active", "inactive", "error"
    last_used: Optional[datetime] = None
    tools_available: List[str] = Field(default_factory=list)
    
class ConversationHistory(BaseModel):
    """Historial de conversación"""
    message_id: str
    user_message: str
    agent_response: str
    agent_used: str
    timestamp: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)

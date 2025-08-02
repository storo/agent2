from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, AsyncGenerator
import asyncio
import json
import uuid
from datetime import datetime

# Importaciones locales
from src.agents.main_agent import MainAgent
from src.core.config import settings
from src.models.schemas import ChatRequest, ChatResponse, StreamChatResponse

app = FastAPI(
    title="Agent VAM API",
    description="Virtual Assistant Manager - Sistema de Agentes Inteligentes",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global del agente principal
main_agent = MainAgent()

@app.on_event("startup")
async def startup_event():
    """Inicialización de la aplicación"""
    await main_agent.initialize()
    print(" Agent VAM API iniciada correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    """Limpieza al cerrar la aplicación"""
    await main_agent.cleanup()
    print(" Agent VAM API cerrada")

@app.get("/")
async def root():
    return {
        "message": "Agent VAM API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Endpoint de salud del sistema"""
    try:
        # Verificar conexiones a servicios
        health_status = await main_agent.health_check()
        return {
            "status": "healthy",
            "services": health_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_sync(
    request: ChatRequest,
    background_tasks: BackgroundTasks
):
    """Endpoint síncrono para chat - respuesta completa"""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Procesar mensaje con el agente principal
        response = await main_agent.process_message(
            message=request.message,
            session_id=session_id,
            user_id=request.user_id,
            context=request.context,
            stream=False
        )
        
        # Guardar en historial en background
        background_tasks.add_task(
            main_agent.save_conversation_history,
            session_id,
            request.message,
            response["content"]
        )
        
        return ChatResponse(
            session_id=session_id,
            message_id=str(uuid.uuid4()),
            content=response["content"],
            agent_used=response["agent_used"],
            tools_used=response.get("tools_used", []),
            metadata=response.get("metadata", {}),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Endpoint de streaming para chat - respuesta en tiempo real"""
    
    async def generate_response() -> AsyncGenerator[str, None]:
        try:
            session_id = request.session_id or str(uuid.uuid4())
            message_id = str(uuid.uuid4())
            
            # Enviar metadata inicial
            initial_data = {
                "type": "start",
                "session_id": session_id,
                "message_id": message_id,
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(initial_data)}\n\n"
            
            # Procesar mensaje con streaming
            async for chunk in main_agent.process_message_stream(
                message=request.message,
                session_id=session_id,
                user_id=request.user_id,
                context=request.context
            ):
                stream_data = {
                    "type": "chunk",
                    "session_id": session_id,
                    "message_id": message_id,
                    "content": chunk["content"],
                    "agent_used": chunk.get("agent_used"),
                    "metadata": chunk.get("metadata", {})
                }
                yield f"data: {json.dumps(stream_data)}\n\n"
            
            # Enviar señal de finalización
            end_data = {
                "type": "end",
                "session_id": session_id,
                "message_id": message_id,
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(end_data)}\n\n"
            
        except Exception as e:
            error_data = {
                "type": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_response(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )

@app.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str, limit: int = 50):
    """Obtener historial de conversación"""
    try:
        history = await main_agent.get_conversation_history(session_id, limit)
        return {
            "session_id": session_id,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """Limpiar sesión y memoria"""
    try:
        await main_agent.clear_session(session_id)
        return {"message": f"Session {session_id} cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing session: {str(e)}")

@app.get("/agents/status")
async def get_agents_status():
    """Estado de todos los sub-agentes"""
    try:
        status = await main_agent.get_agents_status()
        return {
            "main_agent": "active",
            "sub_agents": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting agents status: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

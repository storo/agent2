from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import asyncio
import aioredis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, delete

from src.core.config import settings
from src.models.database import ConversationHistory, SessionMemory

class MemoryManager:
    """Gestor de memoria para conversaciones y sesiones"""
    
    def __init__(self):
        self.redis_client = None
        self.db_engine = None
        self.db_session = None
        
    async def initialize(self):
        """Inicializar conexiones a Redis y PostgreSQL"""
        try:
            # Conexión a Redis
            self.redis_client = aioredis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            
            # Conexión a PostgreSQL
            self.db_engine = create_async_engine(
                settings.database_url,
                echo=settings.debug
            )
            
            self.db_session = sessionmaker(
                self.db_engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            print(" Memory Manager inicializado")
            
        except Exception as e:
            print(f" Error inicializando Memory Manager: {e}")
            raise
    
    async def save_conversation(
        self,
        session_id: str,
        user_message: str,
        agent_response: str,
        agent_used: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Guardar conversación en base de datos"""
        try:
            async with self.db_session() as session:
                conversation = ConversationHistory(
                    session_id=session_id,
                    user_message=user_message,
                    agent_response=agent_response,
                    agent_used=agent_used,
                    metadata=metadata or {},
                    timestamp=datetime.now()
                )
                
                session.add(conversation)
                await session.commit()
                
            # También guardar en Redis para acceso rápido
            await self._cache_conversation(session_id, {
                "user_message": user_message,
                "agent_response": agent_response,
                "agent_used": agent_used,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"Error guardando conversación: {e}")
    
    async def get_conversation_history(
        self, 
        session_id: str, 
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Obtener historial de conversación"""
        try:
            async with self.db_session() as session:
                result = await session.execute(
                    select(ConversationHistory)
                    .where(ConversationHistory.session_id == session_id)
                    .order_by(ConversationHistory.timestamp.desc())
                    .limit(limit)
                )
                
                conversations = result.scalars().all()
                
                return [
                    {
                        "message_id": str(conv.id),
                        "user_message": conv.user_message,
                        "agent_response": conv.agent_response,
                        "agent_used": conv.agent_used,
                        "timestamp": conv.timestamp.isoformat(),
                        "metadata": conv.metadata
                    }
                    for conv in reversed(conversations)
                ]
                
        except Exception as e:
            print(f"Error obteniendo historial: {e}")
            return []
    
    async def get_session_memory(self, session_id: str) -> Dict[str, Any]:
        """Obtener memoria de sesión desde Redis"""
        try:
            memory_key = f"session:{session_id}:memory"
            memory_data = await self.redis_client.get(memory_key)
            
            if memory_data:
                return json.loads(memory_data)
            else:
                # Crear nueva memoria de sesión
                new_memory = {
                    "session_id": session_id,
                    "created_at": datetime.now().isoformat(),
                    "last_activity": datetime.now().isoformat(),
                    "context": {},
                    "preferences": {}
                }
                
                await self.redis_client.setex(
                    memory_key,
                    timedelta(minutes=settings.session_timeout_minutes),
                    json.dumps(new_memory)
                )
                
                return new_memory
                
        except Exception as e:
            print(f"Error obteniendo memoria de sesión: {e}")
            return {}
    
    async def update_session_memory(
        self, 
        session_id: str, 
        updates: Dict[str, Any]
    ):
        """Actualizar memoria de sesión"""
        try:
            memory = await self.get_session_memory(session_id)
            memory.update(updates)
            memory["last_activity"] = datetime.now().isoformat()
            
            memory_key = f"session:{session_id}:memory"
            await self.redis_client.setex(
                memory_key,
                timedelta(minutes=settings.session_timeout_minutes),
                json.dumps(memory)
            )
            
        except Exception as e:
            print(f"Error actualizando memoria de sesión: {e}")
    
    async def clear_session(self, session_id: str):
        """Limpiar sesión de Redis y base de datos"""
        try:
            # Limpiar de Redis
            memory_key = f"session:{session_id}:memory"
            cache_key = f"session:{session_id}:cache"
            
            await self.redis_client.delete(memory_key)
            await self.redis_client.delete(cache_key)
            
            # Opcionalmente limpiar de base de datos
            # (comentado para preservar historial)
            # async with self.db_session() as session:
            #     await session.execute(
            #         delete(ConversationHistory)
            #         .where(ConversationHistory.session_id == session_id)
            #     )
            #     await session.commit()
            
        except Exception as e:
            print(f"Error limpiando sesión: {e}")
    
    async def _cache_conversation(self, session_id: str, conversation: Dict[str, Any]):
        """Cachear conversación en Redis para acceso rápido"""
        try:
            cache_key = f"session:{session_id}:cache"
            
            # Obtener cache existente
            cached_conversations = await self.redis_client.lrange(cache_key, 0, -1)
            
            # Agregar nueva conversación
            await self.redis_client.lpush(cache_key, json.dumps(conversation))
            
            # Mantener solo las últimas 20 conversaciones en cache
            await self.redis_client.ltrim(cache_key, 0, 19)
            
            # Establecer expiración
            await self.redis_client.expire(
                cache_key, 
                timedelta(minutes=settings.session_timeout_minutes)
            )
            
        except Exception as e:
            print(f"Error cacheando conversación: {e}")
    
    async def health_check(self) -> bool:
        """Verificar salud de las conexiones"""
        try:
            # Verificar Redis
            await self.redis_client.ping()
            
            # Verificar PostgreSQL
            async with self.db_session() as session:
                await session.execute("SELECT 1")
            
            return True
            
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    async def cleanup(self):
        """Limpieza de conexiones"""
        try:
            if self.redis_client:
                await self.redis_client.close()
            
            if self.db_engine:
                await self.db_engine.dispose()
                
            print(" Memory Manager limpiado")
            
        except Exception as e:
            print(f"Error en limpieza: {e}")

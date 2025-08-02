from typing import Dict, Any, List, Optional, AsyncGenerator
import asyncio
import json
from datetime import datetime, timedelta
import uuid

from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

from src.core.config import settings
from src.agents.product_agent import ProductAgent
from src.agents.campaign_agent import CampaignAgent
from src.agents.account_agent import AccountAgent
from src.agents.platform_agent import PlatformAgent
from src.agents.analytics_agent import AnalyticsAgent
from src.core.memory_manager import MemoryManager
from src.core.llm_factory import LLMFactory

class AgentState(TypedDict):
    """Estado compartido entre agentes"""
    messages: Annotated[List[BaseMessage], add_messages]
    user_message: str
    session_id: str
    user_id: Optional[str]
    context: Dict[str, Any]
    current_agent: str
    agent_response: str
    tools_used: List[str]
    metadata: Dict[str, Any]
    requires_sub_agent: bool
    sub_agent_type: Optional[str]

class MainAgent:
    """Agente principal que coordina todos los sub-agentes"""
    
    def __init__(self):
        self.llm = None
        self.memory_manager = None
        self.sub_agents = {}
        self.graph = None
        self.sessions = {}  # Cache de sesiones activas
        
    async def initialize(self):
        """Inicializar el agente principal y todos los sub-agentes"""
        try:
            # Inicializar LLM
            self.llm = LLMFactory.create_llm(
                provider=settings.default_llm_provider,
                model=settings.default_model
            )
            
            # Inicializar gestor de memoria
            self.memory_manager = MemoryManager()
            await self.memory_manager.initialize()
            
            # Inicializar sub-agentes
            self.sub_agents = {
                "product": ProductAgent(),
                "campaign": CampaignAgent(),
                "account": AccountAgent(),
                "platform": PlatformAgent(),
                "analytics": AnalyticsAgent()
            }
            
            # Inicializar cada sub-agente
            for agent in self.sub_agents.values():
                await agent.initialize()
            
            # Crear el grafo de decisiones
            self._create_decision_graph()
            
            print(" Agente principal inicializado correctamente")
            
        except Exception as e:
            print(f" Error inicializando agente principal: {e}")
            raise
    
    def _create_decision_graph(self):
        """Crear el grafo de decisiones con LangGraph"""
        workflow = StateGraph(AgentState)
        
        # Nodos del grafo
        workflow.add_node("analyze_intent", self._analyze_intent)
        workflow.add_node("route_to_agent", self._route_to_agent)
        workflow.add_node("process_with_main", self._process_with_main)
        workflow.add_node("process_with_sub", self._process_with_sub_agent)
        workflow.add_node("finalize_response", self._finalize_response)
        
        # Definir el flujo
        workflow.set_entry_point("analyze_intent")
        
        workflow.add_conditional_edges(
            "analyze_intent",
            self._should_use_sub_agent,
            {
                "sub_agent": "route_to_agent",
                "main_agent": "process_with_main"
            }
        )
        
        workflow.add_edge("route_to_agent", "process_with_sub")
        workflow.add_edge("process_with_main", "finalize_response")
        workflow.add_edge("process_with_sub", "finalize_response")
        workflow.add_edge("finalize_response", END)
        
        self.graph = workflow.compile()
    
    async def process_message(
        self,
        message: str,
        session_id: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Procesar mensaje del usuario (modo síncrono)"""
        
        # Preparar estado inicial
        initial_state = AgentState(
            messages=[HumanMessage(content=message)],
            user_message=message,
            session_id=session_id,
            user_id=user_id,
            context=context or {},
            current_agent="main",
            agent_response="",
            tools_used=[],
            metadata={},
            requires_sub_agent=False,
            sub_agent_type=None
        )
        
        # Ejecutar el grafo
        final_state = await self.graph.ainvoke(initial_state)
        
        return {
            "content": final_state["agent_response"],
            "agent_used": final_state["current_agent"],
            "tools_used": final_state["tools_used"],
            "metadata": final_state["metadata"]
        }
    
    async def process_message_stream(
        self,
        message: str,
        session_id: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Procesar mensaje del usuario (modo streaming)"""
        
        # Preparar estado inicial
        initial_state = AgentState(
            messages=[HumanMessage(content=message)],
            user_message=message,
            session_id=session_id,
            user_id=user_id,
            context=context or {},
            current_agent="main",
            agent_response="",
            tools_used=[],
            metadata={},
            requires_sub_agent=False,
            sub_agent_type=None
        )
        
        # Ejecutar el grafo con streaming
        async for state in self.graph.astream(initial_state):
            for node_name, node_state in state.items():
                if "agent_response" in node_state and node_state["agent_response"]:
                    yield {
                        "content": node_state["agent_response"],
                        "agent_used": node_state["current_agent"],
                        "metadata": {
                            "node": node_name,
                            "tools_used": node_state.get("tools_used", [])
                        }
                    }
    
    async def _analyze_intent(self, state: AgentState) -> AgentState:
        """Analizar la intención del usuario"""
        
        analysis_prompt = f"""
        Analiza el siguiente mensaje del usuario y determina:
        1. La intención principal
        2. Si requiere un sub-agente especializado
        3. Qué tipo de sub-agente sería más apropiado
        
        Mensaje: {state["user_message"]}
        
        Sub-agentes disponibles:
        - product: Información sobre productos
        - campaign: Gestión de campañas publicitarias
        - account: Gestión de cuenta de usuario
        - platform: Configuración de plataforma
        - analytics: Análisis y reportes
        
        Responde en formato JSON:
        {{
            "requires_sub_agent": true/false,
            "sub_agent_type": "tipo" o null,
            "confidence": 0.0-1.0,
            "reasoning": "explicación"
        }}
        """
        
        try:
            response = await self.llm.ainvoke(analysis_prompt)
            analysis = json.loads(response.content)
            
            state["requires_sub_agent"] = analysis["requires_sub_agent"]
            state["sub_agent_type"] = analysis.get("sub_agent_type")
            state["metadata"]["intent_analysis"] = analysis
            
        except Exception as e:
            print(f"Error en análisis de intención: {e}")
            state["requires_sub_agent"] = False
            
        return state
    
    def _should_use_sub_agent(self, state: AgentState) -> str:
        """Decidir si usar sub-agente o agente principal"""
        return "sub_agent" if state["requires_sub_agent"] else "main_agent"
    
    async def _route_to_agent(self, state: AgentState) -> AgentState:
        """Enrutar a sub-agente específico"""
        agent_type = state["sub_agent_type"]
        if agent_type and agent_type in self.sub_agents:
            state["current_agent"] = agent_type
        return state
    
    async def _process_with_main(self, state: AgentState) -> AgentState:
        """Procesar con agente principal"""
        
        # Obtener memoria de la sesión
        memory = await self.memory_manager.get_session_memory(state["session_id"])
        
        # Crear prompt con contexto
        system_prompt = """
        Eres el agente principal de Agent VAM, un asistente virtual inteligente.
        Tu rol es ayudar a los usuarios con consultas generales sobre la plataforma,
        productos y servicios. Eres amigable, profesional y siempre buscas la mejor
        manera de ayudar al usuario.
        """
        
        try:
            # Procesar con LLM
            messages = [HumanMessage(content=system_prompt)] + state["messages"]
            response = await self.llm.ainvoke(messages)
            
            state["agent_response"] = response.content
            state["current_agent"] = "main"
            
        except Exception as e:
            state["agent_response"] = f"Lo siento, hubo un error procesando tu solicitud: {str(e)}"
            
        return state
    
    async def _process_with_sub_agent(self, state: AgentState) -> AgentState:
        """Procesar con sub-agente especializado"""
        
        agent_type = state["current_agent"]
        if agent_type in self.sub_agents:
            try:
                sub_agent = self.sub_agents[agent_type]
                response = await sub_agent.process_message(
                    message=state["user_message"],
                    session_id=state["session_id"],
                    context=state["context"]
                )
                
                state["agent_response"] = response["content"]
                state["tools_used"].extend(response.get("tools_used", []))
                state["metadata"].update(response.get("metadata", {}))
                
            except Exception as e:
                state["agent_response"] = f"Error en sub-agente {agent_type}: {str(e)}"
        
        return state
    
    async def _finalize_response(self, state: AgentState) -> AgentState:
        """Finalizar respuesta y guardar en memoria"""
        
        # Guardar en memoria
        await self.memory_manager.save_conversation(
            session_id=state["session_id"],
            user_message=state["user_message"],
            agent_response=state["agent_response"],
            agent_used=state["current_agent"],
            metadata=state["metadata"]
        )
        
        # Actualizar timestamp
        state["metadata"]["processed_at"] = datetime.now().isoformat()
        
        return state
    
    async def health_check(self) -> Dict[str, str]:
        """Verificar salud de todos los servicios"""
        health = {}
        
        # Verificar LLM
        try:
            await self.llm.ainvoke("test")
            health["llm"] = "healthy"
        except:
            health["llm"] = "unhealthy"
        
        # Verificar sub-agentes
        for name, agent in self.sub_agents.items():
            try:
                await agent.health_check()
                health[f"agent_{name}"] = "healthy"
            except:
                health[f"agent_{name}"] = "unhealthy"
        
        # Verificar memoria
        try:
            await self.memory_manager.health_check()
            health["memory"] = "healthy"
        except:
            health["memory"] = "unhealthy"
        
        return health
    
    async def get_conversation_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Obtener historial de conversación"""
        return await self.memory_manager.get_conversation_history(session_id, limit)
    
    async def clear_session(self, session_id: str):
        """Limpiar sesión"""
        await self.memory_manager.clear_session(session_id)
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    async def save_conversation_history(self, session_id: str, user_message: str, agent_response: str):
        """Guardar historial de conversación (para background tasks)"""
        await self.memory_manager.save_conversation(
            session_id=session_id,
            user_message=user_message,
            agent_response=agent_response,
            agent_used="main",
            metadata={"saved_at": datetime.now().isoformat()}
        )
    
    async def get_agents_status(self) -> Dict[str, Dict]:
        """Obtener estado de todos los sub-agentes"""
        status = {}
        for name, agent in self.sub_agents.items():
            try:
                agent_status = await agent.get_status()
                status[name] = agent_status
            except Exception as e:
                status[name] = {"status": "error", "error": str(e)}
        return status
    
    async def cleanup(self):
        """Limpieza al cerrar"""
        if self.memory_manager:
            await self.memory_manager.cleanup()
        
        for agent in self.sub_agents.values():
            await agent.cleanup()

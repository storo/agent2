from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from langchain.schema import BaseMessage, HumanMessage
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI

from src.core.config import settings
from src.core.llm_factory import LLMFactory

class CampaignCreationTool(BaseTool):
    """Herramienta para crear campa�as"""
    name = "create_campaign"
    description = "Crear una nueva campa�a publicitaria"
    
    def _run(self, campaign_data: Dict[str, Any]) -> str:
        # Simular creaci�n de campa�a
        campaign_id = f"camp_{datetime.now().strftime("%Y%m%d_%H%M%S")}"
        return f"Campa�a creada exitosamente con ID: {campaign_id}"
    
    async def _arun(self, campaign_data: Dict[str, Any]) -> str:
        return self._run(campaign_data)

class CampaignOptimizationTool(BaseTool):
    """Herramienta para optimizar campa�as"""
    name = "optimize_campaign"
    description = "Optimizar una campa�a existente"
    
    def _run(self, campaign_id: str, optimization_params: Dict[str, Any]) -> str:
        # Simular optimizaci�n
        return f"Campa�a {campaign_id} optimizada con mejoras en CTR del 15%"
    
    async def _arun(self, campaign_id: str, optimization_params: Dict[str, Any]) -> str:
        return self._run(campaign_id, optimization_params)

class CampaignAgent:
    """Sub-agente especializado en gesti�n de campa�as"""
    
    def __init__(self):
        self.llm = None
        self.tools = []
        self.name = "campaign_agent"
        self.status = "inactive"
        
    async def initialize(self):
        """Inicializar el agente de campa�as"""
        try:
            self.llm = LLMFactory.create_llm(
                provider=settings.default_llm_provider,
                model=settings.default_model
            )
            
            # Inicializar herramientas
            self.tools = [
                CampaignCreationTool(),
                CampaignOptimizationTool()
            ]
            
            self.status = "active"
            print(f" {self.name} inicializado correctamente")
            
        except Exception as e:
            self.status = "error"
            print(f" Error inicializando {self.name}: {e}")
            raise
    
    async def process_message(
        self,
        message: str,
        session_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Procesar mensaje relacionado con campa�as"""
        
        system_prompt = """
        Eres un especialista en gesti�n de campa�as publicitarias. Tu rol es:
        
        1. Ayudar a crear nuevas campa�as publicitarias
        2. Optimizar campa�as existentes
        3. Analizar rendimiento de campa�as
        4. Sugerir mejores pr�cticas
        
        Herramientas disponibles:
        - create_campaign: Para crear nuevas campa�as
        - optimize_campaign: Para optimizar campa�as existentes
        
        Siempre proporciona respuestas detalladas y accionables.
        Si necesitas informaci�n adicional, pregunta espec�ficamente qu� necesitas.
        """
        
        try:
            # Determinar si necesita usar herramientas
            tool_decision = await self._decide_tool_usage(message)
            
            response_content = ""
            tools_used = []
            
            if tool_decision["use_tool"]:
                # Usar herramienta espec�fica
                tool_name = tool_decision["tool_name"]
                tool_params = tool_decision["tool_params"]
                
                tool = next((t for t in self.tools if t.name == tool_name), None)
                if tool:
                    tool_result = await tool._arun(**tool_params)
                    tools_used.append(tool_name)
                    
                    # Generar respuesta basada en el resultado de la herramienta
                    response_content = await self._generate_response_with_tool_result(
                        message, tool_result, tool_name
                    )
                else:
                    response_content = "Lo siento, la herramienta solicitada no est� disponible."
            else:
                # Respuesta directa sin herramientas
                messages = [
                    HumanMessage(content=system_prompt),
                    HumanMessage(content=message)
                ]
                response = await self.llm.ainvoke(messages)
                response_content = response.content
            
            return {
                "content": response_content,
                "tools_used": tools_used,
                "metadata": {
                    "agent": self.name,
                    "session_id": session_id,
                    "tool_decision": tool_decision,
                    "processed_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "content": f"Error procesando solicitud de campa�a: {str(e)}",
                "tools_used": [],
                "metadata": {"error": str(e)}
            }
    
    async def _decide_tool_usage(self, message: str) -> Dict[str, Any]:
        """Decidir si usar herramientas y cu�les"""
        
        decision_prompt = f"""
        Analiza el siguiente mensaje y determina si necesita usar alguna herramienta:
        
        Mensaje: "{message}"
        
        Herramientas disponibles:
        1. create_campaign - Para crear nuevas campa�as
        2. optimize_campaign - Para optimizar campa�as existentes
        
        Responde en formato JSON:
        {{
            "use_tool": true/false,
            "tool_name": "nombre_herramienta" o null,
            "tool_params": {{}} o null,
            "reasoning": "explicaci�n de la decisi�n"
        }}
        """
        
        try:
            response = await self.llm.ainvoke(decision_prompt)
            decision = json.loads(response.content)
            return decision
        except:
            return {"use_tool": False, "tool_name": None, "tool_params": None}
    
    async def _generate_response_with_tool_result(
        self, 
        original_message: str, 
        tool_result: str, 
        tool_name: str
    ) -> str:
        """Generar respuesta basada en resultado de herramienta"""
        
        response_prompt = f"""
        El usuario pregunt�: "{original_message}"
        
        Us� la herramienta "{tool_name}" y obtuve este resultado:
        "{tool_result}"
        
        Genera una respuesta natural y �til para el usuario basada en este resultado.
        Explica qu� se hizo y proporciona pr�ximos pasos si es relevante.
        """
        
        response = await self.llm.ainvoke(response_prompt)
        return response.content
    
    async def health_check(self) -> bool:
        """Verificar salud del agente"""
        try:
            await self.llm.ainvoke("test")
            return True
        except:
            return False
    
    async def get_status(self) -> Dict[str, Any]:
        """Obtener estado del agente"""
        return {
            "name": self.name,
            "status": self.status,
            "tools_available": [tool.name for tool in self.tools],
            "last_health_check": datetime.now().isoformat()
        }
    
    async def cleanup(self):
        """Limpieza del agente"""
        self.status = "inactive"
        print(f" {self.name} limpiado")

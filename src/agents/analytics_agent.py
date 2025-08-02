from typing import Dict, Any, Optional
from src.core.llm_factory import LLMFactory

class AnalyticsAgent:
    def __init__(self):
        self.llm = None
        self.name = "analytics_agent"
        self.status = "inactive"
        
    async def initialize(self):
        self.llm = LLMFactory.create_llm()
        self.status = "active"
        print(f" {self.name} inicializado")
        
    async def process_message(self, message: str, session_id: str, context: Optional[Dict] = None):
        system_prompt = "Eres un especialista en an�lisis y reportes. Ayuda con m�tricas, KPIs, insights y generaci�n de reportes."
        response = await self.llm.ainvoke(f"{system_prompt}\n\nUsuario: {message}")
        return {"content": response.content, "tools_used": [], "metadata": {"agent": self.name}}
        
    async def health_check(self): return True
    async def get_status(self): return {"name": self.name, "status": self.status}
    async def cleanup(self): self.status = "inactive"

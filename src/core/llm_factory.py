from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatAnthropic

from src.core.config import settings

class LLMFactory:
    """Factory para crear instancias de LLM"""
    
    @staticmethod
    def create_llm(provider: str = "openai", model: str = "gpt-4", **kwargs):
        """Crear instancia de LLM según el proveedor"""
        
        if provider == "openai":
            return ChatOpenAI(
                model=model,
                api_key=settings.openai_api_key,
                temperature=0.7,
                **kwargs
            )
        
        elif provider == "anthropic":
            return ChatAnthropic(
                model=model,
                api_key=settings.anthropic_api_key,
                temperature=0.7,
                **kwargs
            )
        
        elif provider == "ollama":
            return Ollama(
                model=settings.ollama_model,
                base_url=settings.ollama_base_url,
                **kwargs
            )
        
        else:
            raise ValueError(f"Proveedor LLM no soportado: {provider}")
    
    @staticmethod
    def get_available_providers() -> list:
        """Obtener lista de proveedores disponibles"""
        return ["openai", "anthropic", "ollama"]

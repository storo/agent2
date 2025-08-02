from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API Configuration
    app_name: str = "Agent VAM"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # LLM Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    default_llm_provider: str = "openai"  # "openai", "anthropic", "ollama"
    default_model: str = "gpt-4"
    
    # Ollama Configuration (for local LLM)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    
    # Database Configuration
    database_url: str = "postgresql://user:password@localhost:5432/agent_vam"
    redis_url: str = "redis://localhost:6379/0"
    
    # Vector Store Configuration
    vector_store_type: str = "pgvector"  # "pgvector", "pinecone", "chroma"
    embedding_model: str = "text-embedding-ada-002"
    
    # Memory Configuration
    max_conversation_history: int = 100
    session_timeout_minutes: int = 60
    
    # Agent Configuration
    max_agent_retries: int = 3
    agent_timeout_seconds: int = 30
    
    # Monitoring
    enable_metrics: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Instancia global de configuración
settings = Settings()

# Validaciones de configuración
def validate_config():
    """Valida la configuración al inicio"""
    if settings.default_llm_provider == "openai" and not settings.openai_api_key:
        raise ValueError("OpenAI API key is required when using OpenAI provider")
    
    if settings.default_llm_provider == "anthropic" and not settings.anthropic_api_key:
        raise ValueError("Anthropic API key is required when using Anthropic provider")
    
    print(f" Configuración validada - Provider: {settings.default_llm_provider}")

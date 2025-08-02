# Agent VAM - Guía de Desarrollo

## Configuración del Entorno de Desarrollo

### 1. Requisitos
- Python 3.9+
- PostgreSQL 14+
- Redis 6+
- Git
- IDE recomendado: VS Code

### 2. Instalación
```bash
# Clonar repositorio
git clone <repository-url>
cd agent-vam

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

### 3. Configuración de Base de Datos
```sql
-- PostgreSQL
CREATE DATABASE agent_vam;
CREATE USER agent_user WITH PASSWORD "password";
GRANT ALL PRIVILEGES ON DATABASE agent_vam TO agent_user;

-- Conectar a la base de datos
\c agent_vam

-- Instalar extensión pgvector
CREATE EXTENSION vector;
```

### 4. Ejecutar en Desarrollo
```bash
# Modo desarrollo con auto-reload
python main.py

# O usando uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Estructura de Código

### Convenciones de Naming
- **Archivos**: snake_case (ej: `main_agent.py`)
- **Clases**: PascalCase (ej: `MainAgent`)
- **Funciones/Variables**: snake_case (ej: `process_message`)
- **Constantes**: UPPER_CASE (ej: `MAX_RETRIES`)

### Organización de Archivos
```
src/
 agents/          # Lógica de agentes
 api/            # Endpoints adicionales
 core/           # Configuración y utilidades
 models/         # Modelos de datos
 tools/          # Herramientas para agentes
```

## Desarrollo de Nuevos Sub-Agentes

### 1. Crear Nuevo Sub-Agente
```python
# src/agents/new_agent.py
from typing import Dict, Any, Optional
from src.core.llm_factory import LLMFactory

class NewAgent:
    def __init__(self):
        self.llm = None
        self.name = "new_agent"
        self.status = "inactive"
        self.tools = []
        
    async def initialize(self):
        """Inicializar el agente"""
        self.llm = LLMFactory.create_llm()
        # Inicializar herramientas
        self.tools = []
        self.status = "active"
        print(f" {self.name} inicializado")
        
    async def process_message(
        self, 
        message: str, 
        session_id: str, 
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Procesar mensaje del usuario"""
        system_prompt = "Eres un especialista en [dominio]. Tu rol es..."
        
        # Lógica de procesamiento
        response = await self.llm.ainvoke(f"{system_prompt}\n\nUsuario: {message}")
        
        return {
            "content": response.content,
            "tools_used": [],
            "metadata": {"agent": self.name}
        }
        
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
            "tools_available": [tool.name for tool in self.tools]
        }
        
    async def cleanup(self):
        """Limpieza del agente"""
        self.status = "inactive"
```

### 2. Registrar en Main Agent
```python
# src/agents/main_agent.py
from src.agents.new_agent import NewAgent

class MainAgent:
    async def initialize(self):
        # ... código existente ...
        
        # Agregar nuevo agente
        self.sub_agents["new"] = NewAgent()
        
        # Inicializar
        for agent in self.sub_agents.values():
            await agent.initialize()
```

## Desarrollo de Herramientas

### 1. Crear Nueva Herramienta
```python
# src/tools/new_tool.py
from langchain.tools import BaseTool
from typing import Dict, Any

class NewTool(BaseTool):
    name = "new_tool"
    description = "Descripción de lo que hace la herramienta"
    
    def _run(self, param1: str, param2: Dict[str, Any]) -> str:
        """Ejecutar herramienta (síncrono)"""
        # Lógica de la herramienta
        result = f"Procesado: {param1}"
        return result
    
    async def _arun(self, param1: str, param2: Dict[str, Any]) -> str:
        """Ejecutar herramienta (asíncrono)"""
        # Versión asíncrona
        return self._run(param1, param2)
```

### 2. Agregar a Sub-Agente
```python
# En el sub-agente correspondiente
from src.tools.new_tool import NewTool

class SomeAgent:
    async def initialize(self):
        self.tools = [
            NewTool(),
            # ... otras herramientas
        ]
```

## Testing

### 1. Configuración de Tests
```python
# tests/conftest.py
import pytest
import asyncio
from src.agents.main_agent import MainAgent

@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def main_agent():
    agent = MainAgent()
    await agent.initialize()
    yield agent
    await agent.cleanup()
```

### 2. Test de Sub-Agente
```python
# tests/test_campaign_agent.py
import pytest
from src.agents.campaign_agent import CampaignAgent

@pytest.mark.asyncio
async def test_campaign_agent_initialization():
    agent = CampaignAgent()
    await agent.initialize()
    
    assert agent.status == "active"
    assert len(agent.tools) > 0
    
    await agent.cleanup()

@pytest.mark.asyncio
async def test_campaign_agent_process_message():
    agent = CampaignAgent()
    await agent.initialize()
    
    response = await agent.process_message(
        message="Crear campaña para producto tech",
        session_id="test_session"
    )
    
    assert "content" in response
    assert response["content"] is not None
    
    await agent.cleanup()
```

### 3. Ejecutar Tests
```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_campaign_agent.py

# Con coverage
pytest --cov=src
```

## Debugging

### 1. Logging
```python
import structlog

logger = structlog.get_logger()

# En tu código
logger.info("Processing message", 
           session_id=session_id, 
           message_length=len(message))

logger.error("Error processing", 
            error=str(e), 
            session_id=session_id)
```

### 2. Debug Mode
```python
# En .env
DEBUG=true
LOG_LEVEL=DEBUG

# Esto habilitará:
# - Logs detallados
# - SQL queries en consola
# - Stack traces completos
```

### 3. Health Checks
```bash
# Verificar estado del sistema
curl http://localhost:8000/health

# Verificar agentes específicos
curl http://localhost:8000/agents/status
```

## Deployment

### 1. Docker
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Docker Compose
```yaml
# docker-compose.yml
version: "3.8"
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/agent_vam
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
      
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: agent_vam
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:6-alpine
    
volumes:
  postgres_data:
```

## Mejores Prácticas

### 1. Código
- Usar type hints en todas las funciones
- Documentar funciones con docstrings
- Manejar errores apropiadamente
- Usar async/await consistentemente

### 2. Agentes
- Cada agente debe tener un dominio específico
- Implementar health checks
- Usar herramientas para acciones específicas
- Mantener estado mínimo

### 3. Performance
- Usar cache para datos frecuentes
- Implementar timeouts apropiados
- Monitorear uso de memoria
- Optimizar queries de base de datos

### 4. Seguridad
- Validar todos los inputs
- No loggear información sensible
- Usar HTTPS en producción
- Implementar rate limiting

# Agent VAM - Gu�a de Instalaci�n

## Requisitos Previos

- Python 3.9+
- PostgreSQL 14+
- Redis 6+
- (Opcional) Ollama para LLM local

## Instalaci�n

### 1. Clonar y configurar el proyecto

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar configuraci�n
cp .env.example .env
```

### 2. Configurar variables de entorno

Editar `.env` con tus credenciales:

```bash
# Configurar API key de OpenAI
OPENAI_API_KEY=sk-your-actual-api-key

# Configurar base de datos
DATABASE_URL=postgresql://username:password@localhost:5432/agent_vam
REDIS_URL=redis://localhost:6379/0
```

### 3. Configurar base de datos

```sql
-- Crear base de datos
CREATE DATABASE agent_vam;

-- Instalar extensi�n pgvector
CREATE EXTENSION vector;
```

### 4. Ejecutar la aplicaci�n

```bash
# Modo desarrollo
python main.py

# Modo producci�n
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Endpoints Disponibles

### Chat S�ncrono
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d {
    "message": "Hola, quiero crear una campa�a",
    "session_id": "test_session",
    "user_id": "user_123"
  }
```

### Chat Streaming
```bash
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d {
    "message": "Expl�came sobre los productos disponibles",
    "session_id": "test_session"
  }
```

### Estado de Salud
```bash
curl http://localhost:8000/health
```

### Estado de Agentes
```bash
curl http://localhost:8000/agents/status
```

## Estructura del Proyecto

```
agent-vam/
 main.py                 # API principal
 requirements.txt        # Dependencias
 .env.example           # Configuraci�n de ejemplo
 README.md              # Documentaci�n
 INSTALL.md             # Esta gu�a
 src/
     agents/            # Sub-agentes especializados
        main_agent.py  # Agente principal
        campaign_agent.py
        product_agent.py
        account_agent.py
        platform_agent.py
        analytics_agent.py
     api/               # Endpoints adicionales
     core/              # Configuraci�n y utilidades
        config.py      # Configuraci�n
        llm_factory.py # Factory para LLMs
        memory_manager.py # Gesti�n de memoria
     models/            # Modelos de datos
         schemas.py     # Esquemas Pydantic
         database.py    # Modelos SQLAlchemy
```

## Caracter�sticas Implementadas

 **API FastAPI con endpoints s�ncronos y streaming**
 **Agente principal con LangGraph para decisiones inteligentes**
 **5 sub-agentes especializados**
 **Gesti�n de memoria con Redis + PostgreSQL**
 **Soporte para m�ltiples LLM providers (OpenAI, Anthropic, Ollama)**
 **Sistema de herramientas para agentes**
 **Health checks y monitoreo**
 **Gesti�n de sesiones y contexto**

## Pr�ximos Pasos

1. Implementar herramientas espec�ficas para cada agente
2. Agregar autenticaci�n y autorizaci�n
3. Implementar vector store para b�squeda sem�ntica
4. Agregar m�tricas y logging avanzado
5. Crear frontend para interacci�n
6. Implementar tests automatizados

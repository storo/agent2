# Agent VAM - Virtual Assistant Manager

> **Sistema de Agentes Inteligentes para Gesti�n de Campa�as, Productos y Plataforma**

Agent VAM es un sistema multi-agente basado en LLM que act�a como puerta de entrada inteligente para usuarios, proporcionando acceso especializado a informaci�n sobre productos, plataforma, cuentas y campa�as a trav�s de sub-agentes especializados.

##  Implementaci�n Completada

### **Stack Tecnol�gico: LangChain + FastAPI + PostgreSQL + Redis**

 **API FastAPI** con endpoints s�ncronos y streaming  
 **Agente Principal** con LangGraph para decisiones inteligentes  
 **5 Sub-agentes Especializados** (Campaign, Product, Account, Platform, Analytics)  
 **Gesti�n de Memoria** con Redis + PostgreSQL  
 **Soporte Multi-LLM** (OpenAI, Anthropic, Ollama)  
 **Sistema de Herramientas** extensible  
 **Health Checks** y monitoreo  
 **Gesti�n de Sesiones** con continuidad conversacional  

##  Documentaci�n

### Gu�as de Usuario
- **[Instalaci�n y Configuraci�n](INSTALL.md)** - C�mo configurar y ejecutar el sistema
- **[API Reference](docs/API.md)** - Documentaci�n completa de endpoints
- **[Ejemplos Pr�cticos](docs/EXAMPLES.md)** - Casos de uso reales y c�digo de ejemplo

### Documentaci�n T�cnica
- **[Arquitectura del Sistema](docs/ARCHITECTURE.md)** - Dise�o t�cnico y patrones implementados
- **[Gu�a de Desarrollo](docs/DEVELOPMENT.md)** - C�mo contribuir y extender el sistema

##  Estructura del Proyecto

```
agent-vam/
  README.md              # Este archivo
  INSTALL.md             # Gu�a de instalaci�n
  requirements.txt       # Dependencias Python
  .env.example          # Configuraci�n de ejemplo
  main.py               # API FastAPI principal
  src/                  # C�digo fuente
     agents/           # Sistema de agentes
       main_agent.py    # Agente coordinador principal
       campaign_agent.py # Gesti�n de campa�as
       product_agent.py  # Informaci�n de productos
       account_agent.py  # Gesti�n de cuentas
       platform_agent.py # Configuraci�n de plataforma
       analytics_agent.py # An�lisis y reportes
     core/             # Infraestructura
       config.py        # Configuraci�n centralizada
       llm_factory.py   # Factory para LLMs
       memory_manager.py # Gesti�n de memoria
     models/           # Modelos de datos
       schemas.py       # Esquemas Pydantic
       database.py      # Modelos SQLAlchemy
     api/             # Endpoints adicionales
  docs/                # Documentaci�n t�cnica
     API.md              # Referencia de API
     ARCHITECTURE.md     # Arquitectura del sistema
     DEVELOPMENT.md      # Gu�a de desarrollo
     EXAMPLES.md         # Ejemplos pr�cticos
```

##  Inicio R�pido

### 1. Instalaci�n
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

### 2. Configurar Servicios
```bash
# PostgreSQL
createdb agent_vam
psql agent_vam -c "CREATE EXTENSION vector;"

# Redis (debe estar ejecut�ndose)
redis-server
```

### 3. Ejecutar
```bash
# Modo desarrollo
python main.py

# La API estar� disponible en http://localhost:8000
```

##  Endpoints Principales

### Chat
- `POST /chat` - Chat s�ncrono con respuesta completa
- `POST /chat/stream` - Chat streaming en tiempo real

### Gesti�n de Sesiones
- `GET /sessions/{id}/history` - Historial de conversaci�n
- `DELETE /sessions/{id}` - Limpiar sesi�n

### Sistema
- `GET /health` - Estado de salud
- `GET /agents/status` - Estado de agentes
- `GET /` - Informaci�n general

##  Ejemplos de Uso

### Chat S�ncrono
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d {
    "message": "Quiero crear una campa�a para mi producto",
    "session_id": "mi_sesion"
  }
```

### Chat Streaming (JavaScript)
```javascript
const response = await fetch('/chat/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Ay�dame con an�lisis de mi campa�a",
    session_id: "mi_sesion"
  })
});

const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(new TextDecoder().decode(value));
}
```

##  Sistema de Agentes

### Agente Principal (MainAgent)
- **Coordinador central** que analiza intenciones del usuario
- **Enrutamiento inteligente** hacia sub-agentes especializados
- **Gesti�n de memoria** y continuidad conversacional
- **Decisiones basadas en LLM** usando LangGraph

### Sub-Agentes Especializados

####  Campaign Agent
- Creaci�n y optimizaci�n de campa�as publicitarias
- An�lisis de audiencias y segmentaci�n
- Recomendaciones de presupuesto y plataformas

####  Product Agent
- Informaci�n detallada sobre productos y servicios
- Comparaci�n de planes y caracter�sticas
- Recomendaciones personalizadas

####  Account Agent
- Gesti�n de cuentas de usuario
- Configuraci�n de perfiles y preferencias
- Soporte t�cnico y resoluci�n de problemas

####  Platform Agent
- Configuraci�n de la plataforma
- Integraciones y APIs
- Gesti�n de permisos y roles

####  Analytics Agent
- An�lisis de rendimiento de campa�as
- Reportes y m�tricas detalladas
- Insights y recomendaciones de optimizaci�n

##  Caracter�sticas T�cnicas

### Decisiones Inteligentes
- **LangGraph**: Flujos de decisi�n basados en LLM
- **Enrutamiento Autom�tico**: El agente principal decide qu� sub-agente usar
- **Coordinaci�n Multi-Agente**: Colaboraci�n entre agentes especializados

### Memoria Persistente
- **Redis**: Cache y memoria a corto plazo
- **PostgreSQL**: Historial y memoria a largo plazo
- **Gesti�n de Sesiones**: Continuidad conversacional

### Flexibilidad LLM
- **OpenAI**: GPT-4, GPT-3.5
- **Anthropic**: Claude
- **Ollama**: Modelos locales (Llama, Mistral, etc.)

### Streaming en Tiempo Real
- **Server-Sent Events**: Respuestas en tiempo real
- **WebSocket Support**: Para integraciones avanzadas
- **Modo Dual**: S�ncrono y as�ncrono seg�n necesidad

### Escalabilidad y Monitoreo
- **Health Checks**: Verificaci�n autom�tica de componentes
- **M�tricas de Rendimiento**: Monitoreo de latencia y throughput
- **Logging Estructurado**: Trazabilidad completa de operaciones
- **Rate Limiting**: Control de carga y protecci�n

##  Tecnolog�as Utilizadas

### Backend
- **FastAPI**: Framework web moderno y r�pido
- **LangChain**: Orquestaci�n de LLMs y agentes
- **LangGraph**: Flujos de trabajo con grafos
- **Pydantic**: Validaci�n de datos
- **SQLAlchemy**: ORM para base de datos

### Base de Datos
- **PostgreSQL**: Base de datos principal con extensi�n vector
- **Redis**: Cache y gesti�n de sesiones
- **pgvector**: B�squeda sem�ntica y embeddings

### LLMs y AI
- **OpenAI API**: GPT-4, GPT-3.5-turbo
- **Anthropic API**: Claude
- **Ollama**: Modelos locales
- **Embeddings**: Para b�squeda sem�ntica

### Infraestructura
- **Docker**: Containerizaci�n
- **Docker Compose**: Orquestaci�n de servicios
- **Uvicorn**: Servidor ASGI
- **Asyncio**: Programaci�n as�ncrona

##  Contribuir

Ver **[Gu�a de Desarrollo](docs/DEVELOPMENT.md)** para:
- Configuraci�n del entorno de desarrollo
- C�mo crear nuevos sub-agentes
- C�mo agregar herramientas
- Testing y debugging
- Mejores pr�cticas

##  Casos de Uso

### Para Marketers
- **Creaci�n de Campa�as**: "Ay�dame a crear una campa�a para mi app de fitness"
- **Optimizaci�n**: "�C�mo puedo mejorar el ROI de mi campa�a actual?"
- **An�lisis**: "Mu�strame el rendimiento de mis campa�as esta semana"

### Para Usuarios de Producto
- **Comparaci�n de Planes**: "�Cu�l es la diferencia entre Basic y Premium?"
- **Configuraci�n**: "�C�mo configuro las integraciones con mi CRM?"
- **Soporte**: "Tengo problemas con la autenticaci�n"

### Para Administradores
- **Gesti�n de Usuarios**: "�C�mo asigno permisos a mi equipo?"
- **Configuraci�n de Plataforma**: "Necesito configurar SSO"
- **Monitoreo**: "�Cu�l es el estado de salud del sistema?"

##  Roadmap

### Pr�ximas Caracter�sticas
- [ ] **Integraci�n con CRMs** (Salesforce, HubSpot)
- [ ] **Webhooks y Eventos** en tiempo real
- [ ] **Dashboard Web** para gesti�n visual
- [ ] **API de Terceros** para integraciones
- [ ] **Modelos Fine-tuned** espec�ficos del dominio
- [ ] **Multilenguaje** y localizaci�n
- [ ] **An�lisis Predictivo** con ML
- [ ] **Automatizaci�n de Workflows**

### Mejoras T�cnicas
- [ ] **Kubernetes** para orquestaci�n
- [ ] **GraphQL** como alternativa a REST
- [ ] **Microservicios** para mayor escalabilidad
- [ ] **Event Sourcing** para auditabilidad
- [ ] **CQRS** para separaci�n de responsabilidades

---

**Agent VAM** - *Tu puerta de entrada inteligente a una plataforma completa de gesti�n de campa�as y productos.*

*Desarrollado con  usando las mejores pr�cticas de AI y desarrollo moderno.*

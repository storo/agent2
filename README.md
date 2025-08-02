# Agent VAM - Virtual Assistant Manager

> **Sistema de Agentes Inteligentes para Gestión de Campañas, Productos y Plataforma**

Agent VAM es un sistema multi-agente basado en LLM que actúa como puerta de entrada inteligente para usuarios, proporcionando acceso especializado a información sobre productos, plataforma, cuentas y campañas a través de sub-agentes especializados.

##  Implementación Completada

### **Stack Tecnológico: LangChain + FastAPI + PostgreSQL + Redis**

 **API FastAPI** con endpoints síncronos y streaming  
 **Agente Principal** con LangGraph para decisiones inteligentes  
 **5 Sub-agentes Especializados** (Campaign, Product, Account, Platform, Analytics)  
 **Gestión de Memoria** con Redis + PostgreSQL  
 **Soporte Multi-LLM** (OpenAI, Anthropic, Ollama)  
 **Sistema de Herramientas** extensible  
 **Health Checks** y monitoreo  
 **Gestión de Sesiones** con continuidad conversacional  

##  Documentación

### Guías de Usuario
- **[Instalación y Configuración](INSTALL.md)** - Cómo configurar y ejecutar el sistema
- **[API Reference](docs/API.md)** - Documentación completa de endpoints
- **[Ejemplos Prácticos](docs/EXAMPLES.md)** - Casos de uso reales y código de ejemplo

### Documentación Técnica
- **[Arquitectura del Sistema](docs/ARCHITECTURE.md)** - Diseño técnico y patrones implementados
- **[Guía de Desarrollo](docs/DEVELOPMENT.md)** - Cómo contribuir y extender el sistema

##  Estructura del Proyecto

```
agent-vam/
  README.md              # Este archivo
  INSTALL.md             # Guía de instalación
  requirements.txt       # Dependencias Python
  .env.example          # Configuración de ejemplo
  main.py               # API FastAPI principal
  src/                  # Código fuente
     agents/           # Sistema de agentes
       main_agent.py    # Agente coordinador principal
       campaign_agent.py # Gestión de campañas
       product_agent.py  # Información de productos
       account_agent.py  # Gestión de cuentas
       platform_agent.py # Configuración de plataforma
       analytics_agent.py # Análisis y reportes
     core/             # Infraestructura
       config.py        # Configuración centralizada
       llm_factory.py   # Factory para LLMs
       memory_manager.py # Gestión de memoria
     models/           # Modelos de datos
       schemas.py       # Esquemas Pydantic
       database.py      # Modelos SQLAlchemy
     api/             # Endpoints adicionales
  docs/                # Documentación técnica
     API.md              # Referencia de API
     ARCHITECTURE.md     # Arquitectura del sistema
     DEVELOPMENT.md      # Guía de desarrollo
     EXAMPLES.md         # Ejemplos prácticos
```

##  Inicio Rápido

### 1. Instalación
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

# Redis (debe estar ejecutándose)
redis-server
```

### 3. Ejecutar
```bash
# Modo desarrollo
python main.py

# La API estará disponible en http://localhost:8000
```

##  Endpoints Principales

### Chat
- `POST /chat` - Chat síncrono con respuesta completa
- `POST /chat/stream` - Chat streaming en tiempo real

### Gestión de Sesiones
- `GET /sessions/{id}/history` - Historial de conversación
- `DELETE /sessions/{id}` - Limpiar sesión

### Sistema
- `GET /health` - Estado de salud
- `GET /agents/status` - Estado de agentes
- `GET /` - Información general

##  Ejemplos de Uso

### Chat Síncrono
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d {
    "message": "Quiero crear una campaña para mi producto",
    "session_id": "mi_sesion"
  }
```

### Chat Streaming (JavaScript)
```javascript
const response = await fetch('/chat/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Ayúdame con análisis de mi campaña",
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
- **Gestión de memoria** y continuidad conversacional
- **Decisiones basadas en LLM** usando LangGraph

### Sub-Agentes Especializados

####  Campaign Agent
- Creación y optimización de campañas publicitarias
- Análisis de audiencias y segmentación
- Recomendaciones de presupuesto y plataformas

####  Product Agent
- Información detallada sobre productos y servicios
- Comparación de planes y características
- Recomendaciones personalizadas

####  Account Agent
- Gestión de cuentas de usuario
- Configuración de perfiles y preferencias
- Soporte técnico y resolución de problemas

####  Platform Agent
- Configuración de la plataforma
- Integraciones y APIs
- Gestión de permisos y roles

####  Analytics Agent
- Análisis de rendimiento de campañas
- Reportes y métricas detalladas
- Insights y recomendaciones de optimización

##  Características Técnicas

### Decisiones Inteligentes
- **LangGraph**: Flujos de decisión basados en LLM
- **Enrutamiento Automático**: El agente principal decide qué sub-agente usar
- **Coordinación Multi-Agente**: Colaboración entre agentes especializados

### Memoria Persistente
- **Redis**: Cache y memoria a corto plazo
- **PostgreSQL**: Historial y memoria a largo plazo
- **Gestión de Sesiones**: Continuidad conversacional

### Flexibilidad LLM
- **OpenAI**: GPT-4, GPT-3.5
- **Anthropic**: Claude
- **Ollama**: Modelos locales (Llama, Mistral, etc.)

### Streaming en Tiempo Real
- **Server-Sent Events**: Respuestas en tiempo real
- **WebSocket Support**: Para integraciones avanzadas
- **Modo Dual**: Síncrono y asíncrono según necesidad

### Escalabilidad y Monitoreo
- **Health Checks**: Verificación automática de componentes
- **Métricas de Rendimiento**: Monitoreo de latencia y throughput
- **Logging Estructurado**: Trazabilidad completa de operaciones
- **Rate Limiting**: Control de carga y protección

##  Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **LangChain**: Orquestación de LLMs y agentes
- **LangGraph**: Flujos de trabajo con grafos
- **Pydantic**: Validación de datos
- **SQLAlchemy**: ORM para base de datos

### Base de Datos
- **PostgreSQL**: Base de datos principal con extensión vector
- **Redis**: Cache y gestión de sesiones
- **pgvector**: Búsqueda semántica y embeddings

### LLMs y AI
- **OpenAI API**: GPT-4, GPT-3.5-turbo
- **Anthropic API**: Claude
- **Ollama**: Modelos locales
- **Embeddings**: Para búsqueda semántica

### Infraestructura
- **Docker**: Containerización
- **Docker Compose**: Orquestación de servicios
- **Uvicorn**: Servidor ASGI
- **Asyncio**: Programación asíncrona

##  Contribuir

Ver **[Guía de Desarrollo](docs/DEVELOPMENT.md)** para:
- Configuración del entorno de desarrollo
- Cómo crear nuevos sub-agentes
- Cómo agregar herramientas
- Testing y debugging
- Mejores prácticas

##  Casos de Uso

### Para Marketers
- **Creación de Campañas**: "Ayúdame a crear una campaña para mi app de fitness"
- **Optimización**: "¿Cómo puedo mejorar el ROI de mi campaña actual?"
- **Análisis**: "Muéstrame el rendimiento de mis campañas esta semana"

### Para Usuarios de Producto
- **Comparación de Planes**: "¿Cuál es la diferencia entre Basic y Premium?"
- **Configuración**: "¿Cómo configuro las integraciones con mi CRM?"
- **Soporte**: "Tengo problemas con la autenticación"

### Para Administradores
- **Gestión de Usuarios**: "¿Cómo asigno permisos a mi equipo?"
- **Configuración de Plataforma**: "Necesito configurar SSO"
- **Monitoreo**: "¿Cuál es el estado de salud del sistema?"

##  Roadmap

### Próximas Características
- [ ] **Integración con CRMs** (Salesforce, HubSpot)
- [ ] **Webhooks y Eventos** en tiempo real
- [ ] **Dashboard Web** para gestión visual
- [ ] **API de Terceros** para integraciones
- [ ] **Modelos Fine-tuned** específicos del dominio
- [ ] **Multilenguaje** y localización
- [ ] **Análisis Predictivo** con ML
- [ ] **Automatización de Workflows**

### Mejoras Técnicas
- [ ] **Kubernetes** para orquestación
- [ ] **GraphQL** como alternativa a REST
- [ ] **Microservicios** para mayor escalabilidad
- [ ] **Event Sourcing** para auditabilidad
- [ ] **CQRS** para separación de responsabilidades

---

**Agent VAM** - *Tu puerta de entrada inteligente a una plataforma completa de gestión de campañas y productos.*

*Desarrollado con  usando las mejores prácticas de AI y desarrollo moderno.*

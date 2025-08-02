# Agent VAM - Arquitectura del Sistema

## Visi�n General

Agent VAM implementa una arquitectura de microservicios basada en agentes inteligentes, donde cada componente tiene responsabilidades espec�ficas y se comunica a trav�s de protocolos bien definidos.

## Componentes Principales

### 1. API Gateway (FastAPI)
- **Archivo**: `main.py`
- **Responsabilidad**: Punto de entrada �nico para todas las requests
- **Caracter�sticas**:
  - Endpoints REST y WebSocket
  - Streaming con Server-Sent Events
  - Middleware CORS
  - Health checks
  - Gesti�n de errores centralizada

### 2. Agente Principal (Main Agent)
- **Archivo**: `src/agents/main_agent.py`
- **Responsabilidad**: Coordinador central y punto de decisi�n
- **Tecnolog�a**: LangGraph para flujos de decisi�n
- **Funciones**:
  - An�lisis de intenci�n del usuario
  - Enrutamiento a sub-agentes
  - Coordinaci�n de respuestas
  - Gesti�n de contexto

### 3. Sub-Agentes Especializados

#### Campaign Agent (`src/agents/campaign_agent.py`)
- **Dominio**: Gesti�n de campa�as publicitarias
- **Herramientas**:
  - `create_campaign`: Crear nuevas campa�as
  - `optimize_campaign`: Optimizar campa�as existentes
- **Casos de uso**: Creaci�n, optimizaci�n, an�lisis de campa�as

#### Product Agent (`src/agents/product_agent.py`)
- **Dominio**: Informaci�n de productos
- **Funciones**: Consultas sobre caracter�sticas, precios, comparaciones

#### Account Agent (`src/agents/account_agent.py`)
- **Dominio**: Gesti�n de cuentas de usuario
- **Funciones**: Configuraciones, facturaci�n, suscripciones

#### Platform Agent (`src/agents/platform_agent.py`)
- **Dominio**: Configuraci�n de plataforma
- **Funciones**: Integraciones, APIs, configuraciones t�cnicas

#### Analytics Agent (`src/agents/analytics_agent.py`)
- **Dominio**: An�lisis y reportes
- **Funciones**: M�tricas, KPIs, insights, generaci�n de reportes

### 4. Gesti�n de Memoria
- **Archivo**: `src/core/memory_manager.py`
- **Tecnolog�as**: Redis + PostgreSQL
- **Funciones**:
  - Memoria a corto plazo (Redis)
  - Memoria a largo plazo (PostgreSQL)
  - Gesti�n de sesiones
  - Cache de conversaciones

### 5. Factory de LLMs
- **Archivo**: `src/core/llm_factory.py`
- **Responsabilidad**: Abstracci�n para m�ltiples proveedores LLM
- **Proveedores soportados**:
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude)
  - Ollama (modelos locales)

## Flujo de Procesamiento

### 1. Recepci�n de Request
```
Usuario  FastAPI  Main Agent
```

### 2. An�lisis de Intenci�n
```
Main Agent  LLM  An�lisis de intenci�n  Decisi�n de enrutamiento
```

### 3. Procesamiento
```
Si requiere sub-agente:
  Main Agent  Sub-Agent  Herramientas  Respuesta
Si no:
  Main Agent  LLM  Respuesta directa
```

### 4. Finalizaci�n
```
Respuesta  Memory Manager  Usuario
```

## Patrones de Dise�o Implementados

### 1. Factory Pattern
- **LLMFactory**: Creaci�n de instancias LLM seg�n proveedor
- **Beneficio**: Flexibilidad para cambiar proveedores sin modificar c�digo

### 2. Strategy Pattern
- **Sub-agentes**: Diferentes estrategias para diferentes dominios
- **Beneficio**: Especializaci�n y escalabilidad

### 3. Observer Pattern
- **Streaming**: Notificaci�n en tiempo real de cambios de estado
- **Beneficio**: Experiencia de usuario reactiva

### 4. Command Pattern
- **Herramientas de agentes**: Encapsulaci�n de acciones espec�ficas
- **Beneficio**: Extensibilidad y reutilizaci�n

## Decisiones Arquitect�nicas

### �Por qu� LangGraph?
- **Ventaja**: Permite flujos de decisi�n complejos basados en LLM
- **Alternativa**: L�gica condicional tradicional
- **Decisi�n**: LLM toma decisiones, no c�digo

### �Por qu� Redis + PostgreSQL?
- **Redis**: Velocidad para memoria a corto plazo y cache
- **PostgreSQL**: Persistencia y b�squeda compleja
- **Alternativa**: Solo PostgreSQL o solo Redis
- **Decisi�n**: H�brido para optimizar rendimiento y persistencia

### �Por qu� FastAPI?
- **Ventajas**: Async nativo, documentaci�n autom�tica, validaci�n
- **Alternativas**: Flask, Django
- **Decisi�n**: Mejor para APIs modernas con streaming

## Escalabilidad

### Horizontal
- **API**: M�ltiples instancias detr�s de load balancer
- **Agentes**: Cada sub-agente puede ejecutarse independientemente
- **Base de datos**: Sharding de PostgreSQL, cluster de Redis

### Vertical
- **LLM**: Modelos m�s grandes o especializados
- **Memoria**: M�s RAM para cache
- **CPU**: M�s cores para procesamiento paralelo

## Monitoreo y Observabilidad

### M�tricas
- **API**: Latencia, throughput, errores
- **Agentes**: Tiempo de procesamiento, uso de herramientas
- **LLM**: Tokens consumidos, latencia de respuesta
- **Memoria**: Hit rate de cache, uso de memoria

### Logging
- **Estructurado**: JSON logs con contexto
- **Niveles**: DEBUG, INFO, WARNING, ERROR
- **Correlaci�n**: Trace ID para seguir requests

### Health Checks
- **Endpoint**: `/health`
- **Verificaciones**: LLM, base de datos, Redis, sub-agentes
- **Respuesta**: Estado de cada servicio

## Seguridad

### Autenticaci�n (Futuro)
- **JWT tokens**: Para usuarios autenticados
- **API keys**: Para integraciones

### Autorizaci�n (Futuro)
- **RBAC**: Roles y permisos
- **Rate limiting**: Prevenci�n de abuso

### Datos
- **Encriptaci�n**: En tr�nsito (HTTPS) y en reposo
- **Sanitizaci�n**: Validaci�n de inputs
- **Logs**: Sin informaci�n sensible

## Extensibilidad

### Nuevos Sub-Agentes
1. Crear clase heredando de base agent
2. Implementar m�todos requeridos
3. Registrar en main agent
4. Agregar herramientas espec�ficas

### Nuevas Herramientas
1. Heredar de `BaseTool`
2. Implementar `_run` y `_arun`
3. Agregar a sub-agente correspondiente

### Nuevos LLM Providers
1. Agregar en `LLMFactory`
2. Configurar en `config.py`
3. Actualizar documentaci�n

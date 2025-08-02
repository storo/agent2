# Agent VAM - Arquitectura del Sistema

## Visión General

Agent VAM implementa una arquitectura de microservicios basada en agentes inteligentes, donde cada componente tiene responsabilidades específicas y se comunica a través de protocolos bien definidos.

## Componentes Principales

### 1. API Gateway (FastAPI)
- **Archivo**: `main.py`
- **Responsabilidad**: Punto de entrada único para todas las requests
- **Características**:
  - Endpoints REST y WebSocket
  - Streaming con Server-Sent Events
  - Middleware CORS
  - Health checks
  - Gestión de errores centralizada

### 2. Agente Principal (Main Agent)
- **Archivo**: `src/agents/main_agent.py`
- **Responsabilidad**: Coordinador central y punto de decisión
- **Tecnología**: LangGraph para flujos de decisión
- **Funciones**:
  - Análisis de intención del usuario
  - Enrutamiento a sub-agentes
  - Coordinación de respuestas
  - Gestión de contexto

### 3. Sub-Agentes Especializados

#### Campaign Agent (`src/agents/campaign_agent.py`)
- **Dominio**: Gestión de campañas publicitarias
- **Herramientas**:
  - `create_campaign`: Crear nuevas campañas
  - `optimize_campaign`: Optimizar campañas existentes
- **Casos de uso**: Creación, optimización, análisis de campañas

#### Product Agent (`src/agents/product_agent.py`)
- **Dominio**: Información de productos
- **Funciones**: Consultas sobre características, precios, comparaciones

#### Account Agent (`src/agents/account_agent.py`)
- **Dominio**: Gestión de cuentas de usuario
- **Funciones**: Configuraciones, facturación, suscripciones

#### Platform Agent (`src/agents/platform_agent.py`)
- **Dominio**: Configuración de plataforma
- **Funciones**: Integraciones, APIs, configuraciones técnicas

#### Analytics Agent (`src/agents/analytics_agent.py`)
- **Dominio**: Análisis y reportes
- **Funciones**: Métricas, KPIs, insights, generación de reportes

### 4. Gestión de Memoria
- **Archivo**: `src/core/memory_manager.py`
- **Tecnologías**: Redis + PostgreSQL
- **Funciones**:
  - Memoria a corto plazo (Redis)
  - Memoria a largo plazo (PostgreSQL)
  - Gestión de sesiones
  - Cache de conversaciones

### 5. Factory de LLMs
- **Archivo**: `src/core/llm_factory.py`
- **Responsabilidad**: Abstracción para múltiples proveedores LLM
- **Proveedores soportados**:
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude)
  - Ollama (modelos locales)

## Flujo de Procesamiento

### 1. Recepción de Request
```
Usuario  FastAPI  Main Agent
```

### 2. Análisis de Intención
```
Main Agent  LLM  Análisis de intención  Decisión de enrutamiento
```

### 3. Procesamiento
```
Si requiere sub-agente:
  Main Agent  Sub-Agent  Herramientas  Respuesta
Si no:
  Main Agent  LLM  Respuesta directa
```

### 4. Finalización
```
Respuesta  Memory Manager  Usuario
```

## Patrones de Diseño Implementados

### 1. Factory Pattern
- **LLMFactory**: Creación de instancias LLM según proveedor
- **Beneficio**: Flexibilidad para cambiar proveedores sin modificar código

### 2. Strategy Pattern
- **Sub-agentes**: Diferentes estrategias para diferentes dominios
- **Beneficio**: Especialización y escalabilidad

### 3. Observer Pattern
- **Streaming**: Notificación en tiempo real de cambios de estado
- **Beneficio**: Experiencia de usuario reactiva

### 4. Command Pattern
- **Herramientas de agentes**: Encapsulación de acciones específicas
- **Beneficio**: Extensibilidad y reutilización

## Decisiones Arquitectónicas

### ¿Por qué LangGraph?
- **Ventaja**: Permite flujos de decisión complejos basados en LLM
- **Alternativa**: Lógica condicional tradicional
- **Decisión**: LLM toma decisiones, no código

### ¿Por qué Redis + PostgreSQL?
- **Redis**: Velocidad para memoria a corto plazo y cache
- **PostgreSQL**: Persistencia y búsqueda compleja
- **Alternativa**: Solo PostgreSQL o solo Redis
- **Decisión**: Híbrido para optimizar rendimiento y persistencia

### ¿Por qué FastAPI?
- **Ventajas**: Async nativo, documentación automática, validación
- **Alternativas**: Flask, Django
- **Decisión**: Mejor para APIs modernas con streaming

## Escalabilidad

### Horizontal
- **API**: Múltiples instancias detrás de load balancer
- **Agentes**: Cada sub-agente puede ejecutarse independientemente
- **Base de datos**: Sharding de PostgreSQL, cluster de Redis

### Vertical
- **LLM**: Modelos más grandes o especializados
- **Memoria**: Más RAM para cache
- **CPU**: Más cores para procesamiento paralelo

## Monitoreo y Observabilidad

### Métricas
- **API**: Latencia, throughput, errores
- **Agentes**: Tiempo de procesamiento, uso de herramientas
- **LLM**: Tokens consumidos, latencia de respuesta
- **Memoria**: Hit rate de cache, uso de memoria

### Logging
- **Estructurado**: JSON logs con contexto
- **Niveles**: DEBUG, INFO, WARNING, ERROR
- **Correlación**: Trace ID para seguir requests

### Health Checks
- **Endpoint**: `/health`
- **Verificaciones**: LLM, base de datos, Redis, sub-agentes
- **Respuesta**: Estado de cada servicio

## Seguridad

### Autenticación (Futuro)
- **JWT tokens**: Para usuarios autenticados
- **API keys**: Para integraciones

### Autorización (Futuro)
- **RBAC**: Roles y permisos
- **Rate limiting**: Prevención de abuso

### Datos
- **Encriptación**: En tránsito (HTTPS) y en reposo
- **Sanitización**: Validación de inputs
- **Logs**: Sin información sensible

## Extensibilidad

### Nuevos Sub-Agentes
1. Crear clase heredando de base agent
2. Implementar métodos requeridos
3. Registrar en main agent
4. Agregar herramientas específicas

### Nuevas Herramientas
1. Heredar de `BaseTool`
2. Implementar `_run` y `_arun`
3. Agregar a sub-agente correspondiente

### Nuevos LLM Providers
1. Agregar en `LLMFactory`
2. Configurar en `config.py`
3. Actualizar documentación

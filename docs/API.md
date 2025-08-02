# Agent VAM - API Reference

## Endpoints

### Chat Endpoints

#### POST /chat
Chat s�ncrono con respuesta completa.

**Request Body:**
```json
{
  "message": "string",
  "session_id": "string (optional)",
  "user_id": "string (optional)",
  "context": {
    "platform": "web",
    "language": "es"
  }
}
```

**Response:**
```json
{
  "session_id": "string",
  "message_id": "string",
  "content": "string",
  "agent_used": "string",
  "tools_used": ["string"],
  "metadata": {},
  "timestamp": "string"
}
```

#### POST /chat/stream
Chat con streaming en tiempo real usando Server-Sent Events.

**Request Body:** Igual que `/chat`

**Response:** Server-Sent Events (SSE)
```
data: {"type": "start", "session_id": "...", "message_id": "..."}
data: {"type": "chunk", "content": "Hola, voy a ayudarte...", "agent_used": "main"}
data: {"type": "end", "session_id": "...", "message_id": "..."}
```

### System Endpoints

#### GET /health
Verificar estado de salud del sistema.

#### GET /agents/status
Estado de todos los sub-agentes.

#### GET /sessions/{session_id}/history
Obtener historial de conversaci�n.

#### DELETE /sessions/{session_id}
Limpiar sesi�n y memoria.

## Ejemplos de Uso

### Crear Campa�a
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d {
    "message": "Quiero crear una campa�a para mi producto de tecnolog�a",
    "session_id": "user_session_123"
  }
```

### Streaming Chat
```javascript
const response = await fetch("/chat/stream", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    message: "Ay�dame con an�lisis de mi campa�a",
    session_id: "session_123"
  })
});

const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(new TextDecoder().decode(value));
}
```

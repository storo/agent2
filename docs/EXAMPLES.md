# Agent VAM - Ejemplos Pr�cticos

## Casos de Uso Reales

### 1. Crear Campa�a Publicitaria

#### Conversaci�n Completa
```
Usuario: "Hola, quiero crear una campa�a para promocionar mi nuevo producto de tecnolog�a"

Agente Principal: Analiza  Detecta intenci�n de campa�a  Enruta a Campaign Agent

Campaign Agent: "�Perfecto! Te ayudo a crear una campa�a para tu producto tecnol�gico. 
Para crear la mejor campa�a posible, necesito algunos detalles:

1. �Qu� tipo de producto tecnol�gico es?
2. �Cu�l es tu presupuesto aproximado?
3. �Cu�l es tu audiencia objetivo?
4. �En qu� plataformas quieres promocionarlo?"

Usuario: "Es una app m�vil para fitness, presupuesto de $5000, dirigido a personas de 25-40 a�os activas, principalmente Instagram y Facebook"

Campaign Agent: Usa herramienta create_campaign  
"Excelente! He creado una campa�a optimizada para tu app de fitness:

 **Campa�a: FitApp Launch**
 **Presupuesto**: $5,000
 **Audiencia**: Adultos 25-40 a�os, interesados en fitness
 **Plataformas**: Instagram, Facebook
 **Estrategia**: 
- 60% Instagram (contenido visual)
- 40% Facebook (targeting detallado)
- Creativos: Videos de ejercicios, testimonios
- CTA: 'Descarga gratis'

�Te gustar�a que optimice alg�n aspecto espec�fico?"
```

#### Request API
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d {
    "message": "Quiero crear una campa�a para mi app de fitness, presupuesto $5000, audiencia 25-40 a�os",
    "session_id": "campaign_session_001",
    "user_id": "user_123",
    "context": {
      "product_type": "mobile_app",
      "industry": "fitness"
    }
  }
```

#### Response
```json
{
  "session_id": "campaign_session_001",
  "message_id": "msg_456",
  "content": "He creado una campa�a optimizada para tu app de fitness...",
  "agent_used": "campaign",
  "tools_used": ["create_campaign"],
  "metadata": {
    "campaign_id": "camp_20250108_001",
    "estimated_reach": 50000,
    "platforms": ["instagram", "facebook"]
  },
  "timestamp": "2025-01-08T21:30:00Z"
}
```

### 2. Consulta de Producto

#### Conversaci�n
```
Usuario: "�Cu�les son las diferencias entre los planes Basic y Premium?"

Agente Principal: Analiza  Detecta consulta de producto  Enruta a Product Agent

Product Agent: "Te explico las principales diferencias entre nuestros planes:

 **Plan Basic**:
- Hasta 3 campa�as activas
- Audiencia m�xima: 10,000 personas
- Reportes b�sicos
- Soporte por email
- $29/mes

 **Plan Premium**:
- Campa�as ilimitadas
- Audiencia ilimitada
- Reportes avanzados con IA
- Soporte prioritario 24/7
- A/B testing autom�tico
- Optimizaci�n en tiempo real
- $99/mes

 **Recomendaci�n**: Si planeas m�s de 3 campa�as o necesitas an�lisis detallados, Premium te dar� mejor ROI.

�Te gustar�a que calcule cu�l ser�a m�s rentable para tu caso espec�fico?"
```

### 3. An�lisis de Rendimiento

#### Conversaci�n
```
Usuario: "�C�mo est� funcionando mi campa�a de la semana pasada?"

Agente Principal: Analiza  Detecta consulta de analytics  Enruta a Analytics Agent

Analytics Agent: "Aqu� tienes el an�lisis de tu campa�a 'FitApp Launch' de la semana pasada:

 **M�tricas Principales**:
- Impresiones: 45,230 (+12% vs objetivo)
- Clicks: 2,156 (CTR: 4.77%)
- Conversiones: 89 (CPA: $56.18)
- ROAS: 3.2x

 **Insights**:
 Instagram super� expectativas (CTR 6.1%)
 Facebook tuvo menor engagement (CTR 3.2%)
 Videos de ejercicios tuvieron 40% m�s clicks

 **Recomendaciones**:
1. Aumentar presupuesto en Instagram (+30%)
2. Crear m�s contenido de video
3. Ajustar targeting en Facebook

�Quieres que implemente estas optimizaciones autom�ticamente?"
```

### 4. Streaming en Tiempo Real

#### JavaScript Client
```javascript
// Ejemplo de cliente streaming
class AgentVAMClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }
  
  async streamChat(message, sessionId, onChunk, onComplete, onError) {
    try {
      const response = await fetch(`${this.baseUrl}/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          session_id: sessionId
        })
      });
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              if (data.type === 'chunk') {
                onChunk(data.content, data);
              } else if (data.type === 'end') {
                onComplete(data);
                return;
              } else if (data.type === 'error') {
                onError(new Error(data.error));
                return;
              }
            } catch (e) {
              // Ignorar l�neas malformadas
            }
          }
        }
      }
    } catch (error) {
      onError(error);
    }
  }
}

// Uso
const client = new AgentVAMClient();

client.streamChat(
  "Ay�dame a optimizar mi campa�a actual",
  "session_123",
  
  // onChunk
  (content, data) => {
    console.log('Chunk:', content);
    document.getElementById('response').innerHTML += content;
  },
  
  // onComplete
  (data) => {
    console.log('Conversaci�n completada:', data);
  },
  
  // onError
  (error) => {
    console.error('Error:', error);
  }
);
```

### 5. Gesti�n de Sesiones

#### Obtener Historial
```bash
# Obtener �ltimas 10 conversaciones
curl "http://localhost:8000/sessions/user_session_123/history?limit=10"
```

#### Response
```json
{
  "session_id": "user_session_123",
  "history": [
    {
      "message_id": "msg_001",
      "user_message": "Hola, quiero crear una campa�a",
      "agent_response": "�Hola! Te ayudo a crear una campa�a...",
      "agent_used": "campaign",
      "timestamp": "2025-01-08T20:00:00Z",
      "metadata": {}
    },
    {
      "message_id": "msg_002",
      "user_message": "Es para una app de fitness",
      "agent_response": "Perfecto, las apps de fitness...",
      "agent_used": "campaign",
      "timestamp": "2025-01-08T20:01:00Z",
      "metadata": {"campaign_type": "app_promotion"}
    }
  ],
  "count": 2
}
```

#### Limpiar Sesi�n
```bash
curl -X DELETE "http://localhost:8000/sessions/user_session_123"
```

## Integraci�n con Frontend

### React Component
```jsx
import React, { useState, useEffect } from 'react';
import { AgentVAMClient } from './agent-vam-client';

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  
  const client = new AgentVAMClient();
  
  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsStreaming(true);
    
    let assistantMessage = { role: 'assistant', content: '' };
    setMessages(prev => [...prev, assistantMessage]);
    
    await client.streamChat(
      input,
      sessionId,
      
      // onChunk
      (content) => {
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1].content += content;
          return newMessages;
        });
      },
      
      // onComplete
      () => {
        setIsStreaming(false);
      },
      
      // onError
      (error) => {
        console.error('Error:', error);
        setIsStreaming(false);
      }
    );
  };
  
  return (
    <div className="chat-interface">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="content">{msg.content}</div>
          </div>
        ))}
        {isStreaming && <div className="typing-indicator">Escribiendo...</div>}
      </div>
      
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Escribe tu mensaje..."
          disabled={isStreaming}
        />
        <button onClick={sendMessage} disabled={isStreaming}>
          Enviar
        </button>
      </div>
    </div>
  );
}

export default ChatInterface;
```

## Monitoreo y Debugging

### Health Check Script
```python
#!/usr/bin/env python3
import asyncio
import aiohttp
import json

async def check_health():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://localhost:8000/health') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(" Sistema saludable")
                    print(json.dumps(data, indent=2))
                else:
                    print(f" Sistema no saludable: {resp.status}")
        except Exception as e:
            print(f" Error conectando: {e}")

if __name__ == "__main__":
    asyncio.run(check_health())
```

### Load Testing
```python
import asyncio
import aiohttp
import time

async def test_endpoint(session, message_num):
    payload = {
        "message": f"Test message {message_num}",
        "session_id": f"test_session_{message_num}"
    }
    
    start_time = time.time()
    try:
        async with session.post(
            'http://localhost:8000/chat',
            json=payload
        ) as resp:
            await resp.json()
            duration = time.time() - start_time
            print(f"Message {message_num}: {duration:.2f}s")
    except Exception as e:
        print(f"Message {message_num} failed: {e}")

async def load_test(concurrent_requests=10):
    async with aiohttp.ClientSession() as session:
        tasks = [
            test_endpoint(session, i) 
            for i in range(concurrent_requests)
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(load_test(50))
```

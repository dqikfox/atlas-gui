# ULTRON Agent Web Dashboard

A modern, responsive web interface for the ULTRON Agent AI Assistant framework.

## 🎯 Features

### Core Interface
- **Multi-Provider AI Chat** - OpenAI, Anthropic, NVIDIA NIM, Ollama (Local)
- **Real-time System Monitoring** - CPU, Memory, Disk usage
- **Voice Controls** - Speech-to-text and text-to-speech integration
- **Automation Tools** - Screenshot, OCR, Web Search, File Operations
- **Activity Logging** - Comprehensive activity tracking with proper chronological ordering
- **WebSocket Integration** - Real-time updates and communications

### Advanced Features
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Theme** - Professional ULTRON-themed interface
- **Real-time Metrics** - Live system performance monitoring
- **Model Status** - Dynamic AI provider status checking
- **Voice Integration** - Full voice interaction capabilities
- **Automation Hub** - Central control for all automation features

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install fastapi uvicorn websockets aiohttp psutil
```

### 2. Integration with Existing ULTRON Agent

Place these files in your ULTRON Agent root directory:
- `ultron-web-dashboard.html`
- `ultron-dashboard.js`
- `ultron_web_server.py`

### 3. Start the Web Server

```bash
python ultron_web_server.py
```

### 4. Access Dashboard

Open your browser and navigate to:
```
http://localhost:8000
```

## 🔧 Configuration

### Backend Integration

The web server automatically detects and integrates with existing ULTRON components:

```python
# The server will attempt to import:
from agent_core import UltronAgent
from ai_config import AIConfig
from voice_manager import VoiceManager
from vision import VisionManager
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/status` | GET | System status |
| `/chat` | POST | AI chat interface |
| `/voice/start` | POST | Start voice listening |
| `/voice/stop` | POST | Stop voice listening |
| `/automation/screenshot` | POST | Take screenshot |
| `/automation/ocr` | POST | Perform OCR |
| `/models/ollama` | GET | Get Ollama models |
| `/ws` | WebSocket | Real-time updates |

### WebSocket Events

```javascript
// System metrics update
{
  "type": "system_metrics",
  "metrics": {
    "cpu": 25.5,
    "memory": 67.2,
    "disk": 45.8
  }
}

// AI response
{
  "type": "ai_response",
  "response": "Hello! How can I help you?",
  "provider": "openai"
}

// Voice status update
{
  "type": "voice_status",
  "status": {
    "listening": true,
    "message": "Voice listening started"
  }
}
```

## 🎨 Customization

### Theming

The dashboard uses CSS custom properties for easy theming:

```css
:root {
  --ultron-primary: #00ff88;
  --ultron-secondary: #00aaff;
  --ultron-bg-primary: #0a0a0a;
  --ultron-bg-secondary: #1a1a1a;
  /* ... more variables */
}
```

### Adding Custom Tools

1. Add button to automation section in HTML
2. Implement handler in JavaScript
3. Add backend endpoint in Python server

Example:

```javascript
// JavaScript handler
async function customTool() {
    const response = await fetch('/custom/tool', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'custom_action' })
    });
    // Handle response
}
```

```python
# Python endpoint
@app.post("/custom/tool")
async def custom_tool():
    # Implement custom functionality
    return {"status": "success", "message": "Custom tool executed"}
```

## 🔐 Security Features

- **CORS Protection** - Configurable cross-origin policies
- **Input Validation** - Pydantic models for request validation
- **Error Handling** - Comprehensive error handling and logging
- **WebSocket Security** - Connection management and cleanup

## 📱 Mobile Support

The dashboard is fully responsive and supports:
- Touch interactions
- Mobile-optimized layouts
- Swipe gestures
- Responsive typography

## 🔧 Troubleshooting

### Common Issues

1. **"ULTRON components not found"**
   - Ensure the web server is in the same directory as your ULTRON Agent
   - Check import paths in `ultron_web_server.py`

2. **"WebSocket connection failed"**
   - Verify the server is running on port 8000
   - Check firewall settings

3. **"Ollama models not loading"**
   - Ensure Ollama is running: `ollama serve`
   - Check Ollama is accessible at `localhost:11434`

### Debug Mode

Run with debug logging:

```bash
python ultron_web_server.py --log-level debug
```

## 📊 Performance

- **WebSocket Updates** - Real-time with minimal latency
- **System Monitoring** - Updates every 5 seconds
- **Memory Efficient** - Automatic log rotation (last 100 entries)
- **Responsive UI** - Optimized animations and transitions

## 🌟 Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 📄 License

This web dashboard integrates with the existing ULTRON Agent project and follows the same licensing terms.

## 🤝 Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Submit a pull request

---

**Built for ULTRON Agent v2.1.0+**

*The future of AI assistance is here. Experience it through the web.*
/**
 * ULTRON Agent Web Dashboard JavaScript
 * Integrates with existing ULTRON Agent backend APIs
 */

class UltronDashboard {
    constructor() {
        this.apiBase = 'http://localhost:8009'; // Adjust to your FastAPI server
        this.websocket = null;
        this.isListening = false;
        this.currentProvider = 'openai';
        this.activityLogs = [];
        
        this.init();
    }

    async init() {
        this.setupEventListeners();
        this.startTimeUpdater();
        this.loadAIModels();
        this.connectWebSocket();
        this.startSystemMonitoring();
        
        // Initial system check
        this.addLog('system', 'ULTRON Agent dashboard initialized');
        this.checkSystemStatus();
    }

    setupEventListeners() {
        // Chat functionality
        document.getElementById('sendBtn').addEventListener('click', () => this.sendMessage());
        document.getElementById('chatInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        // Provider selection
        document.getElementById('providerSelect').addEventListener('change', (e) => {
            this.currentProvider = e.target.value;
            this.addLog('system', `Switched to ${e.target.value} provider`);
        });

        // Voice controls
        document.getElementById('startListening').addEventListener('click', () => this.startVoiceListening());
        document.getElementById('stopListening').addEventListener('click', () => this.stopVoiceListening());
        document.getElementById('voiceToggle').addEventListener('click', () => this.toggleVoiceMode());

        // Automation tools
        document.querySelectorAll('.ultron-btn').forEach(btn => {
            if (btn.textContent.includes('Screenshot')) {
                btn.addEventListener('click', () => this.takeScreenshot());
            } else if (btn.textContent.includes('OCR')) {
                btn.addEventListener('click', () => this.performOCR());
            } else if (btn.textContent.includes('Web Search')) {
                btn.addEventListener('click', () => this.openWebSearch());
            } else if (btn.textContent.includes('File Ops')) {
                btn.addEventListener('click', () => this.openFileOperations());
            }
        });

        // Clear log
        document.getElementById('clearLog').addEventListener('click', () => this.clearActivityLog());
    }

    startTimeUpdater() {
        const updateTime = () => {
            const now = new Date();
            document.getElementById('currentTime').textContent = now.toLocaleTimeString('en-US', {
                hour12: false,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        };
        updateTime();
        setInterval(updateTime, 1000);
    }

    async loadAIModels() {
        const models = [
            {
                id: 'openai',
                name: 'OpenAI',
                models: ['gpt-4', 'gpt-3.5-turbo'],
                status: 'online',
                icon: 'fas fa-brain',
                color: 'text-blue-400'
            },
            {
                id: 'anthropic',
                name: 'Anthropic',
                models: ['claude-3-opus', 'claude-3-sonnet'],
                status: 'online',
                icon: 'fas fa-robot',
                color: 'text-purple-400'
            },
            {
                id: 'nvidia',
                name: 'NVIDIA NIM',
                models: ['llama-3.1-70b', 'mixtral-8x7b'],
                status: 'online',
                icon: 'fas fa-microchip',
                color: 'text-green-400'
            },
            {
                id: 'ollama',
                name: 'Ollama (Local)',
                models: await this.getOllamaModels(),
                status: 'checking',
                icon: 'fas fa-server',
                color: 'text-yellow-400'
            }
        ];

        const grid = document.getElementById('aiModelsGrid');
        grid.innerHTML = models.map(model => this.createModelCard(model)).join('');
        
        // Check Ollama status
        this.checkOllamaStatus();
    }

    async getOllamaModels() {
        try {
            const response = await fetch('http://localhost:11434/api/tags');
            if (response.ok) {
                const data = await response.json();
                return data.models?.map(m => m.name) || ['No models found'];
            }
        } catch (error) {
            console.log('Ollama not available:', error);
        }
        return ['Ollama not running'];
    }

    createModelCard(model) {
        const statusIcon = model.status === 'online' ? 'fa-circle text-green-400' : 
                          model.status === 'offline' ? 'fa-circle text-red-400' : 
                          'fa-circle text-yellow-400 pulse';

        return `
            <div class="ai-model-card ${model.id === this.currentProvider ? 'active' : ''}" data-provider="${model.id}">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center space-x-2">
                        <i class="${model.icon} ${model.color}"></i>
                        <h4 class="font-semibold">${model.name}</h4>
                    </div>
                    <i class="fas ${statusIcon}"></i>
                </div>
                <div class="text-sm text-gray-400 space-y-1">
                    ${model.models.slice(0, 3).map(m => `<div>• ${m}</div>`).join('')}
                    ${model.models.length > 3 ? `<div class="text-xs">+${model.models.length - 3} more</div>` : ''}
                </div>
            </div>
        `;
    }

    async checkOllamaStatus() {
        try {
            const response = await fetch('http://localhost:11434/api/tags');
            const card = document.querySelector('[data-provider="ollama"]');
            const statusIcon = card.querySelector('.fa-circle');
            
            if (response.ok) {
                statusIcon.className = 'fas fa-circle text-green-400';
                this.addLog('system', 'Ollama local models available');
            } else {
                statusIcon.className = 'fas fa-circle text-red-400';
            }
        } catch (error) {
            const card = document.querySelector('[data-provider="ollama"]');
            const statusIcon = card.querySelector('.fa-circle');
            statusIcon.className = 'fas fa-circle text-red-400';
            this.addLog('error', 'Ollama connection failed - local models unavailable');
        }
    }

    connectWebSocket() {
        try {
            this.websocket = new WebSocket('ws://localhost:8009/ws');
            
            this.websocket.onopen = () => {
                this.addLog('system', 'WebSocket connection established');
            };
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };
            
            this.websocket.onclose = () => {
                this.addLog('warning', 'WebSocket connection closed');
                // Attempt to reconnect after 5 seconds
                setTimeout(() => this.connectWebSocket(), 5000);
            };
        } catch (error) {
            this.addLog('error', 'WebSocket connection failed - real-time updates disabled');
        }
    }

    handleWebSocketMessage(data) {
        switch (data.type) {
            case 'system_metrics':
                this.updateSystemMetrics(data.metrics);
                break;
            case 'voice_status':
                this.updateVoiceStatus(data.status);
                break;
            case 'ai_response':
                this.displayAIResponse(data.response, data.provider);
                break;
            case 'automation_result':
                this.addLog('system', `Automation completed: ${data.message}`);
                break;
        }
    }

    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        input.value = '';
        this.displayMessage('user', message);
        this.addLog('user', message);
        
        try {
            const response = await fetch(`${this.apiBase}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    provider: this.currentProvider,
                    include_voice: this.isVoiceMode
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                this.displayMessage('ai', data.response, this.currentProvider);
                this.addLog('ai', data.response, this.currentProvider);
            } else {
                this.displayMessage('error', 'Failed to get AI response');
                this.addLog('error', 'AI request failed');
            }
        } catch (error) {
            this.displayMessage('error', 'Connection error');
            this.addLog('error', `Connection error: ${error.message}`);
        }
    }

    displayMessage(type, content, provider = null) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `log-entry log-${type} p-3 rounded-lg mb-2`;
        
        const timestamp = new Date().toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const icon = {
            user: '👤',
            ai: '🤖',
            system: '⚙️',
            error: '❌'
        }[type] || '📝';
        
        messageDiv.innerHTML = `
            <div class="flex items-start space-x-3">
                <span class="text-lg">${icon}</span>
                <div class="flex-1">
                    <div class="flex items-center space-x-2 mb-1">
                        <span class="font-medium text-sm uppercase">${type}</span>
                        <span class="text-xs text-gray-400">${timestamp}</span>
                        ${provider ? `<span class="text-xs bg-gray-700 px-2 py-1 rounded">${provider}</span>` : ''}
                    </div>
                    <div class="text-sm">${content}</div>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    addLog(type, message, provider = null) {
        const log = {
            id: Date.now(),
            timestamp: new Date(),
            type: type,
            message: message,
            provider: provider
        };
        
        this.activityLogs.push(log);
        
        // Keep only last 100 logs
        if (this.activityLogs.length > 100) {
            this.activityLogs.shift();
        }
        
        this.renderActivityLog();
    }

    renderActivityLog() {
        const logContainer = document.getElementById('activityLog');
        const logs = this.activityLogs.slice(-20); // Show last 20 logs
        
        logContainer.innerHTML = logs.map(log => {
            const timestamp = log.timestamp.toLocaleTimeString('en-US', {
                hour12: false,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            
            const icon = {
                user: '👤',
                ai: '🤖',
                system: '⚙️',
                error: '❌',
                warning: '⚠️'
            }[log.type] || '📝';
            
            return `
                <div class="log-entry log-${log.type} p-3 rounded-lg">
                    <div class="flex items-start space-x-2">
                        <span>${icon}</span>
                        <div class="flex-1">
                            <div class="flex items-center space-x-2 mb-1">
                                <span class="font-medium text-xs uppercase">${log.type}</span>
                                <span class="text-xs text-gray-400">${timestamp}</span>
                                ${log.provider ? `<span class="text-xs bg-gray-700 px-1 py-0.5 rounded">${log.provider}</span>` : ''}
                            </div>
                            <div class="text-sm">${log.message}</div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        
        logContainer.scrollTop = logContainer.scrollHeight;
    }

    clearActivityLog() {
        this.activityLogs = [];
        this.renderActivityLog();
        this.addLog('system', 'Activity log cleared');
    }

    async startVoiceListening() {
        try {
            const response = await fetch(`${this.apiBase}/voice/start`, {
                method: 'POST'
            });
            
            if (response.ok) {
                this.isListening = true;
                document.getElementById('startListening').disabled = true;
                document.getElementById('stopListening').disabled = false;
                this.addLog('system', 'Voice listening started');
            }
        } catch (error) {
            this.addLog('error', 'Failed to start voice listening');
        }
    }

    async stopVoiceListening() {
        try {
            const response = await fetch(`${this.apiBase}/voice/stop`, {
                method: 'POST'
            });
            
            if (response.ok) {
                this.isListening = false;
                document.getElementById('startListening').disabled = false;
                document.getElementById('stopListening').disabled = true;
                this.addLog('system', 'Voice listening stopped');
            }
        } catch (error) {
            this.addLog('error', 'Failed to stop voice listening');
        }
    }

    toggleVoiceMode() {
        this.isVoiceMode = !this.isVoiceMode;
        const btn = document.getElementById('voiceToggle');
        btn.classList.toggle('ultron-btn-primary');
        this.addLog('system', `Voice mode ${this.isVoiceMode ? 'enabled' : 'disabled'}`);
    }

    async takeScreenshot() {
        try {
            const response = await fetch(`${this.apiBase}/automation/screenshot`, {
                method: 'POST'
            });
            
            if (response.ok) {
                const data = await response.json();
                this.addLog('system', `Screenshot saved: ${data.filename}`);
            }
        } catch (error) {
            this.addLog('error', 'Screenshot failed');
        }
    }

    async performOCR() {
        try {
            const response = await fetch(`${this.apiBase}/automation/ocr`, {
                method: 'POST'
            });
            
            if (response.ok) {
                const data = await response.json();
                this.addLog('system', `OCR completed: ${data.text?.substring(0, 100)}...`);
            }
        } catch (error) {
            this.addLog('error', 'OCR failed');
        }
    }

    openWebSearch() {
        const query = prompt('Enter search query:');
        if (query) {
            this.addLog('system', `Web search initiated: ${query}`);
            // Implement web search functionality
        }
    }

    openFileOperations() {
        this.addLog('system', 'File operations panel opened');
        // Implement file operations UI
    }

    async checkSystemStatus() {
        try {
            const response = await fetch(`${this.apiBase}/status`);
            if (response.ok) {
                const data = await response.json();
                this.addLog('system', `System status: ${data.status}`);
            }
        } catch (error) {
            this.addLog('warning', 'Unable to connect to ULTRON backend');
        }
    }

    startSystemMonitoring() {
        // Simulate system metrics (replace with real API calls)
        setInterval(() => {
            const cpu = Math.floor(Math.random() * 100);
            const memory = Math.floor(Math.random() * 100);
            const disk = Math.floor(Math.random() * 100);
            
            this.updateSystemMetrics({ cpu, memory, disk });
        }, 3000);
    }

    updateSystemMetrics(metrics) {
        document.getElementById('cpuUsage').textContent = `${metrics.cpu}%`;
        document.getElementById('cpuBar').style.width = `${metrics.cpu}%`;
        
        document.getElementById('memoryUsage').textContent = `${metrics.memory}%`;
        document.getElementById('memoryBar').style.width = `${metrics.memory}%`;
        
        document.getElementById('diskUsage').textContent = `${metrics.disk}%`;
        document.getElementById('diskBar').style.width = `${metrics.disk}%`;
    }

    updateVoiceStatus(status) {
        document.getElementById('ttsEngine').textContent = status.tts_engine || 'ElevenLabs';
        document.getElementById('sttEngine').textContent = status.stt_engine || 'Whisper';
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new UltronDashboard();
});
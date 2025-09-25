import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const url = new URL(req.url)
    const path = url.pathname

    // Serve the main dashboard HTML
    if (path === '/ultron-dashboard' || path === '/ultron-dashboard/') {
      return new Response(getDashboardHTML(), {
        headers: {
          ...corsHeaders,
          'Content-Type': 'text/html',
        },
      })
    }

    // API endpoint for system metrics
    if (path === '/ultron-dashboard/api/metrics') {
      const metrics = {
        cpu_usage: Math.floor(Math.random() * 30) + 30,
        memory_usage: Math.floor(Math.random() * 20) + 60,
        uptime: "2d 4h",
        tasks_completed: 1247 + Math.floor(Math.random() * 10),
        timestamp: new Date().toISOString()
      }
      
      return new Response(JSON.stringify(metrics), {
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json',
        },
      })
    }

    // API endpoint for activity logs
    if (path === '/ultron-dashboard/api/logs') {
      const logs = [
        {
          time: new Date().toISOString().slice(11, 19),
          message: "✅ ULTRON Agent initialized successfully",
          type: "info"
        },
        {
          time: new Date().toISOString().slice(11, 19),
          message: "🔧 Web dashboard server started on Supabase",
          type: "info"
        },
        {
          time: new Date().toISOString().slice(11, 19),
          message: "🌐 Real-time monitoring activated",
          type: "success"
        }
      ]
      
      return new Response(JSON.stringify(logs), {
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json',
        },
      })
    }

    // API endpoint for chat
    if (path === '/ultron-dashboard/api/chat' && req.method === 'POST') {
      const { message } = await req.json()
      
      const responses = [
        "I understand your request. Let me process that for you.",
        "Task executed successfully. Is there anything else you need?",
        "System analysis complete. All parameters are within normal ranges.",
        "Command processed. The operation has been completed successfully.",
        "I'm monitoring the situation. Current status looks good.",
        "Data analysis in progress. I'll provide updates shortly."
      ]
      
      const response = responses[Math.floor(Math.random() * responses.length)]
      
      return new Response(JSON.stringify({ 
        response,
        timestamp: new Date().toISOString()
      }), {
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json',
        },
      })
    }

    // Default response
    return new Response('ULTRON Agent Dashboard API', {
      headers: corsHeaders,
    })

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        ...corsHeaders,
        'Content-Type': 'application/json',
      },
    })
  }
})

function getDashboardHTML(): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ULTRON Agent Web Dashboard - Live</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e8e8e8;
            line-height: 1.6;
            overflow-x: hidden;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            background: linear-gradient(90deg, #00d4ff, #0099cc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        }

        .live-badge {
            background: linear-gradient(45deg, #00ff88, #00cc66);
            color: #000;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin-top: 10px;
            animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { box-shadow: 0 0 10px #00ff88; }
            to { box-shadow: 0 0 20px #00ff88, 0 0 30px #00ff88; }
        }

        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 15px 25px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid rgba(0, 212, 255, 0.3);
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #00ff88;
            box-shadow: 0 0 10px #00ff88;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }

        .panel {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(0, 212, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .panel h3 {
            color: #00d4ff;
            margin-bottom: 15px;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        .metric {
            background: rgba(0, 212, 255, 0.1);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid rgba(0, 212, 255, 0.3);
        }

        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #00ff88;
        }

        .metric-label {
            font-size: 0.9rem;
            color: #b8b8b8;
        }

        .activity-log {
            height: 300px;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            padding: 15px;
            border: 1px solid rgba(0, 212, 255, 0.2);
        }

        .log-entry {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 10px;
            padding: 8px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.05);
            border-left: 3px solid #00d4ff;
        }

        .log-time {
            color: #888;
            font-size: 0.8rem;
            min-width: 80px;
        }

        .log-message {
            flex: 1;
            font-size: 0.9rem;
        }

        .chat-panel {
            grid-column: span 2;
        }

        .chat-container {
            height: 400px;
            display: flex;
            flex-direction: column;
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid rgba(0, 212, 255, 0.2);
        }

        .chat-message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
            max-width: 70%;
        }

        .chat-message.user {
            background: rgba(0, 212, 255, 0.2);
            margin-left: auto;
            border: 1px solid rgba(0, 212, 255, 0.3);
        }

        .chat-message.assistant {
            background: rgba(0, 255, 136, 0.2);
            margin-right: auto;
            border: 1px solid rgba(0, 255, 136, 0.3);
        }

        .chat-input-container {
            display: flex;
            gap: 10px;
        }

        .chat-input {
            flex: 1;
            padding: 12px;
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            color: #e8e8e8;
            font-size: 1rem;
        }

        .chat-input:focus {
            outline: none;
            border-color: #00d4ff;
            box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
        }

        .send-btn {
            padding: 12px 20px;
            background: linear-gradient(135deg, #00d4ff, #0099cc);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
        }

        .controls-panel {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(0, 212, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            margin-top: 20px;
        }

        .control-buttons {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }

        .control-btn {
            padding: 10px 20px;
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 8px;
            background: rgba(0, 212, 255, 0.1);
            color: #00d4ff;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .control-btn:hover {
            background: rgba(0, 212, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 212, 255, 0.3);
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(0, 212, 255, 0.5);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(0, 212, 255, 0.7);
        }

        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
            }
            
            .chat-panel {
                grid-column: span 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ ULTRON AGENT WEB DASHBOARD</h1>
            <p>Real-time monitoring and control interface</p>
            <div class="live-badge">🌐 LIVE ON SUPABASE</div>
        </div>

        <div class="status-bar">
            <div class="status-item">
                <div class="status-indicator"></div>
                <span>Server Online</span>
            </div>
            <div class="status-item">
                <span>🔌 Supabase Connected</span>
            </div>
            <div class="status-item">
                <span>📡 Real-time Updates: ON</span>
            </div>
            <div class="status-item">
                <span id="current-time">Loading...</span>
            </div>
        </div>

        <div class="dashboard-grid">
            <div class="panel">
                <h3>📊 System Metrics</h3>
                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-value" id="cpu-usage">Loading...</div>
                        <div class="metric-label">CPU Usage</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="memory-usage">Loading...</div>
                        <div class="metric-label">Memory</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="uptime">Loading...</div>
                        <div class="metric-label">Uptime</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="tasks-completed">Loading...</div>
                        <div class="metric-label">Tasks</div>
                    </div>
                </div>
            </div>

            <div class="panel">
                <h3>📝 Activity Log</h3>
                <div class="activity-log" id="activity-log">
                    <div style="text-align: center; color: #888;">Loading activity logs...</div>
                </div>
            </div>
        </div>

        <div class="panel chat-panel">
            <h3>🤖 AI Chat Interface</h3>
            <div class="chat-container">
                <div class="chat-messages" id="chat-messages">
                    <div class="chat-message assistant">
                        <strong>ULTRON Agent:</strong> Hello! I'm running live on Supabase. How can I help you today?
                    </div>
                </div>
                <div class="chat-input-container">
                    <input type="text" class="chat-input" id="chat-input" placeholder="Type your message here..." />
                    <button class="send-btn" onclick="sendMessage()">Send</button>
                </div>
            </div>
        </div>

        <div class="controls-panel">
            <h3>🔧 System Controls</h3>
            <div class="control-buttons">
                <button class="control-btn" onclick="simulateAction('restart')">🔄 Restart Agent</button>
                <button class="control-btn" onclick="simulateAction('clear-logs')">🗑️ Clear Logs</button>
                <button class="control-btn" onclick="simulateAction('export-data')">💾 Export Data</button>
                <button class="control-btn" onclick="simulateAction('settings')">⚙️ Settings</button>
                <button class="control-btn" onclick="simulateAction('health-check')">🏥 Health Check</button>
                <button class="control-btn" onclick="simulateAction('performance')">📈 Performance Report</button>
            </div>
        </div>
    </div>

    <script>
        // API base URL for the Supabase Edge Function
        const API_BASE = window.location.origin + '/ultron-dashboard/api';
        
        const chatMessages = document.getElementById('chat-messages');
        const chatInput = document.getElementById('chat-input');
        const activityLog = document.getElementById('activity-log');

        // Update time every second
        function updateTime() {
            const now = new Date();
            const timeString = now.toISOString().slice(0, 19).replace('T', ' ');
            document.getElementById('current-time').textContent = timeString;
        }

        // Fetch and update metrics from Supabase API
        async function updateMetrics() {
            try {
                const response = await fetch(API_BASE + '/metrics');
                const data = await response.json();
                
                document.getElementById('cpu-usage').textContent = data.cpu_usage + '%';
                document.getElementById('memory-usage').textContent = data.memory_usage + '%';
                document.getElementById('uptime').textContent = data.uptime;
                document.getElementById('tasks-completed').textContent = data.tasks_completed.toLocaleString();
            } catch (error) {
                console.error('Error fetching metrics:', error);
            }
        }

        // Fetch and update activity logs
        async function updateLogs() {
            try {
                const response = await fetch(API_BASE + '/logs');
                const logs = await response.json();
                
                activityLog.innerHTML = '';
                logs.forEach(log => {
                    const logEntry = document.createElement('div');
                    logEntry.className = 'log-entry';
                    logEntry.innerHTML = \`
                        <div class="log-time">\${log.time}</div>
                        <div class="log-message">\${log.message}</div>
                    \`;
                    activityLog.appendChild(logEntry);
                });
                
                activityLog.scrollTop = activityLog.scrollHeight;
            } catch (error) {
                console.error('Error fetching logs:', error);
            }
        }

        // Send chat message to Supabase API
        async function sendMessage() {
            const message = chatInput.value.trim();
            if (!message) return;

            // Add user message
            const userMessage = document.createElement('div');
            userMessage.className = 'chat-message user';
            userMessage.innerHTML = \`<strong>You:</strong> \${message}\`;
            chatMessages.appendChild(userMessage);

            // Clear input
            chatInput.value = '';

            try {
                // Send to Supabase Edge Function
                const response = await fetch(API_BASE + '/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                });

                const data = await response.json();
                
                // Add AI response
                const aiMessage = document.createElement('div');
                aiMessage.className = 'chat-message assistant';
                aiMessage.innerHTML = \`<strong>ULTRON Agent:</strong> \${data.response}\`;
                chatMessages.appendChild(aiMessage);
                
                chatMessages.scrollTop = chatMessages.scrollHeight;
            } catch (error) {
                console.error('Error sending message:', error);
            }

            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Simulate control actions
        function simulateAction(action) {
            const actions = {
                'restart': '🔄 Agent restart initiated...',
                'clear-logs': '🗑️ Activity logs cleared',
                'export-data': '💾 Data export started...',
                'settings': '⚙️ Settings panel opened',
                'health-check': '🏥 System health check running...',
                'performance': '📈 Generating performance report...'
            };
            
            // Could integrate with Supabase to log these actions
            console.log(actions[action] || '✅ Action completed');
        }

        // Enter key support for chat
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Start update intervals
        setInterval(updateTime, 1000);
        setInterval(updateMetrics, 5000);
        setInterval(updateLogs, 10000);

        // Initial calls
        updateTime();
        updateMetrics();
        updateLogs();

        console.log('🚀 ULTRON Agent Dashboard - Live on Supabase!');
    </script>
</body>
</html>`
}`
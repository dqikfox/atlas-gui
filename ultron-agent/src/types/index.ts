// Core types for the Ultron Agent application

export interface ActivityLog {
  id: string;
  timestamp: Date;
  type: 'user' | 'ai' | 'system';
  message: string;
  provider?: string;
  model?: string;
}

export interface SystemMetrics {
  cpu: number;
  memory: number;
  disk: number;
}

export interface AIProvider {
  id: string;
  name: string;
  models: string[];
  isLocal?: boolean;
  status: 'online' | 'offline' | 'error';
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface AutomationCommand {
  id: string;
  command: string;
  description: string;
  parameters?: Record<string, any>;
}

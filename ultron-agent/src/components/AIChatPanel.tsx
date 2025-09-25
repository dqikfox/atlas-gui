import React, { useState } from 'react';
import { MessageSquare, Send, Loader } from 'lucide-react';
import { ChatMessage, AIProvider } from '../types';

interface AIChatPanelProps {
  messages: ChatMessage[];
  isLoading: boolean;
  currentProvider: string;
  currentModel: string;
  providers: AIProvider[];
  onSendMessage: (message: string) => void;
  onSwitchProvider: (providerId: string, model?: string) => void;
  onClearChat: () => void;
}

export const AIChatPanel: React.FC<AIChatPanelProps> = ({
  messages,
  isLoading,
  currentProvider,
  currentModel,
  providers,
  onSendMessage,
  onSwitchProvider,
  onClearChat
}) => {
  const [inputMessage, setInputMessage] = useState('');
  const [selectedProvider, setSelectedProvider] = useState(currentProvider);
  const [selectedModel, setSelectedModel] = useState(currentModel);

  const handleSend = () => {
    if (inputMessage.trim() && !isLoading) {
      onSendMessage(inputMessage.trim());
      setInputMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleProviderChange = (providerId: string) => {
    setSelectedProvider(providerId);
    const provider = providers.find(p => p.id === providerId);
    if (provider && provider.models.length > 0) {
      const defaultModel = provider.models[0];
      setSelectedModel(defaultModel);
      onSwitchProvider(providerId, defaultModel);
    }
  };

  const handleModelChange = (model: string) => {
    setSelectedModel(model);
    onSwitchProvider(selectedProvider, model);
  };

  const currentProviderData = providers.find(p => p.id === selectedProvider);

  return (
    <div className="panel">
      <div className="panel-header">
        <h3 className="panel-title">
          <MessageSquare size={20} />
          AI Chat
        </h3>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <select
            className="select"
            value={selectedProvider}
            onChange={(e) => handleProviderChange(e.target.value)}
            style={{ fontSize: '0.8rem', padding: '4px 8px' }}
          >
            {providers.map(provider => (
              <option key={provider.id} value={provider.id}>
                {provider.name} 
                {provider.isLocal && ' (Local)'}
                {provider.status === 'offline' && ' (Offline)'}
              </option>
            ))}
          </select>
          
          {currentProviderData && currentProviderData.models.length > 1 && (
            <select
              className="select"
              value={selectedModel}
              onChange={(e) => handleModelChange(e.target.value)}
              style={{ fontSize: '0.8rem', padding: '4px 8px' }}
            >
              {currentProviderData.models.map(model => (
                <option key={model} value={model}>
                  {model}
                </option>
              ))}
            </select>
          )}
          
          <button className="button" onClick={onClearChat}>
            Clear
          </button>
        </div>
      </div>
      
      <div className="panel-content">
        <div className="scrollable" style={{ height: 'calc(100% - 60px)', marginBottom: '10px' }}>
          {messages.length === 0 ? (
            <div style={{ 
              color: '#666', 
              textAlign: 'center', 
              padding: '20px',
              fontStyle: 'italic'
            }}>
              Start a conversation with your AI assistant...
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className="fade-in"
                style={{
                  padding: '12px',
                  marginBottom: '8px',
                  background: message.role === 'user' 
                    ? 'rgba(0, 170, 255, 0.1)' 
                    : 'rgba(0, 255, 136, 0.1)',
                  borderRadius: '8px',
                  borderLeft: `3px solid ${message.role === 'user' ? '#00aaff' : '#00ff88'}`,
                  fontSize: '0.9rem',
                  lineHeight: '1.5'
                }}
              >
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  marginBottom: '6px'
                }}>
                  <span>{message.role === 'user' ? '👤' : '🤖'}</span>
                  <span style={{
                    color: message.role === 'user' ? '#00aaff' : '#00ff88',
                    fontWeight: '600',
                    textTransform: 'capitalize'
                  }}>
                    {message.role}
                  </span>
                  <span style={{
                    color: '#999',
                    fontSize: '0.8rem'
                  }}>
                    {message.timestamp.toLocaleTimeString('en-US', {
                      hour12: false,
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </span>
                </div>
                <div style={{ 
                  color: '#ddd',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word'
                }}>
                  {message.content}
                </div>
              </div>
            ))
          )}
          
          {isLoading && (
            <div style={{
              padding: '12px',
              textAlign: 'center',
              color: '#00ff88'
            }}>
              <Loader className="loading" size={20} style={{ marginRight: '8px' }} />
              AI is thinking...
            </div>
          )}
        </div>
        
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            className="input"
            placeholder="Type your message..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            style={{ flex: 1 }}
          />
          <button
            className="button primary"
            onClick={handleSend}
            disabled={!inputMessage.trim() || isLoading}
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

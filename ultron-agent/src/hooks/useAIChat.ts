import { useState, useCallback } from 'react';
import { ChatMessage, AIProvider } from '../types';

/**
 * Hook to manage AI chat functionality with multiple providers
 */
export const useAIChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentProvider, setCurrentProvider] = useState<string>('openai');
  const [currentModel, setCurrentModel] = useState<string>('gpt-3.5-turbo');

  // Available AI providers
  const providers: AIProvider[] = [
    {
      id: 'openai',
      name: 'OpenAI',
      models: ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
      status: 'online'
    },
    {
      id: 'anthropic',
      name: 'Anthropic',
      models: ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku'],
      status: 'online'
    },
    {
      id: 'google',
      name: 'Google',
      models: ['gemini-pro', 'gemini-pro-vision'],
      status: 'online'
    },
    {
      id: 'groq',
      name: 'Groq',
      models: ['llama2-70b-4096', 'mixtral-8x7b-32768'],
      status: 'online'
    },
    {
      id: 'ollama',
      name: 'Ollama (Local)',
      models: ['llama2', 'codellama', 'mistral'],
      isLocal: true,
      status: 'offline'
    }
  ];

  // Send a message to the AI
  const sendMessage = useCallback(async (content: string, onLogAdd?: (log: any) => void) => {
    setIsLoading(true);
    
    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    // Log user message
    onLogAdd?.({
      type: 'user',
      message: content,
      provider: currentProvider,
      model: currentModel
    });

    try {
      // Call the Supabase Edge Function
      const response = await fetch('/api/ai-chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content,
          provider: currentProvider,
          model: currentModel,
          history: messages.slice(-10) // Send last 10 messages for context
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      const aiMessage: ChatMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, aiMessage]);
      
      // Log AI response
      onLogAdd?.({
        type: 'ai',
        message: data.response,
        provider: currentProvider,
        model: currentModel
      });
      
    } catch (error) {
      console.error('AI Chat Error:', error);
      
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
      
      // Log error
      onLogAdd?.({
        type: 'system',
        message: `AI Chat Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        provider: currentProvider,
        model: currentModel
      });
    } finally {
      setIsLoading(false);
    }
  }, [currentProvider, currentModel, messages]);

  // Clear chat history
  const clearChat = useCallback(() => {
    setMessages([]);
  }, []);

  // Switch provider
  const switchProvider = useCallback((providerId: string, model?: string) => {
    setCurrentProvider(providerId);
    const provider = providers.find(p => p.id === providerId);
    if (provider && provider.models.length > 0) {
      setCurrentModel(model || provider.models[0]);
    }
  }, [providers]);

  return {
    messages,
    isLoading,
    currentProvider,
    currentModel,
    providers,
    sendMessage,
    clearChat,
    switchProvider
  };
};

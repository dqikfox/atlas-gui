import React, { useState } from 'react';
import { Settings, Play, Square, MousePointer, Keyboard } from 'lucide-react';
import { AutomationCommand } from '../types';

interface AutomationPanelProps {
  onLogAdd: (log: any) => void;
}

export const AutomationPanel: React.FC<AutomationPanelProps> = ({ onLogAdd }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [selectedCommand, setSelectedCommand] = useState('');
  
  const automationCommands: AutomationCommand[] = [
    {
      id: 'click',
      command: 'click',
      description: 'Click at coordinates',
      parameters: { x: 0, y: 0 }
    },
    {
      id: 'type',
      command: 'type',
      description: 'Type text',
      parameters: { text: '' }
    },
    {
      id: 'screenshot',
      command: 'screenshot',
      description: 'Take screenshot'
    },
    {
      id: 'scroll',
      command: 'scroll',
      description: 'Scroll page',
      parameters: { direction: 'down', amount: 3 }
    }
  ];

  const executeCommand = async (command: AutomationCommand) => {
    onLogAdd({
      type: 'system',
      message: `Executing automation: ${command.description}`
    });

    try {
      // Simulate automation execution
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      onLogAdd({
        type: 'system',
        message: `Automation completed: ${command.description}`
      });
    } catch (error) {
      onLogAdd({
        type: 'system',
        message: `Automation failed: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    }
  };

  const startRecording = () => {
    setIsRecording(true);
    onLogAdd({
      type: 'system',
      message: 'Started recording automation sequence'
    });
  };

  const stopRecording = () => {
    setIsRecording(false);
    onLogAdd({
      type: 'system',
      message: 'Stopped recording automation sequence'
    });
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <h3 className="panel-title">
          <Settings size={20} />
          Automation
        </h3>
        <div style={{ display: 'flex', gap: '8px' }}>
          {!isRecording ? (
            <button className="button" onClick={startRecording}>
              <Play size={14} style={{ marginRight: '4px' }} />
              Record
            </button>
          ) : (
            <button className="button" onClick={stopRecording} style={{ background: '#ff4444' }}>
              <Square size={14} style={{ marginRight: '4px' }} />
              Stop
            </button>
          )}
        </div>
      </div>
      
      <div className="panel-content">
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '6px', fontSize: '0.9rem' }}>
            Quick Commands:
          </label>
          <select
            className="select"
            value={selectedCommand}
            onChange={(e) => setSelectedCommand(e.target.value)}
            style={{ width: '100%' }}
          >
            <option value="">Select a command...</option>
            {automationCommands.map(cmd => (
              <option key={cmd.id} value={cmd.id}>
                {cmd.description}
              </option>
            ))}
          </select>
        </div>
        
        {selectedCommand && (
          <button
            className="button primary"
            onClick={() => {
              const cmd = automationCommands.find(c => c.id === selectedCommand);
              if (cmd) executeCommand(cmd);
            }}
            style={{ width: '100%', marginBottom: '16px' }}
          >
            Execute Command
          </button>
        )}
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: '1fr 1fr', 
          gap: '8px',
          marginBottom: '16px'
        }}>
          <button
            className="button"
            onClick={() => executeCommand({
              id: 'screenshot',
              command: 'screenshot',
              description: 'Take screenshot'
            })}
          >
            <MousePointer size={14} style={{ marginRight: '4px' }} />
            Screenshot
          </button>
          
          <button
            className="button"
            onClick={() => onLogAdd({
              type: 'system',
              message: 'Keyboard input detection active'
            })}
          >
            <Keyboard size={14} style={{ marginRight: '4px' }} />
            Key Monitor
          </button>
        </div>
        
        {isRecording && (
          <div style={{
            padding: '12px',
            background: 'rgba(255, 170, 0, 0.1)',
            borderRadius: '6px',
            fontSize: '0.8rem',
            color: '#ffaa00',
            textAlign: 'center'
          }}>
            🔴 Recording automation sequence...
          </div>
        )}
        
        <div style={{
          marginTop: '16px',
          fontSize: '0.8rem',
          color: '#999',
          lineHeight: '1.4'
        }}>
          <strong>PyAutoGUI Integration:</strong><br />
          • Mouse control and clicking<br />
          • Keyboard input simulation<br />
          • Screen capture and analysis<br />
          • Window management
        </div>
      </div>
    </div>
  );
};

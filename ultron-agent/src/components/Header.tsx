import React from 'react';
import { Zap, Shield, Wifi, AlertCircle } from 'lucide-react';

interface HeaderProps {
  systemStatus: 'online' | 'offline' | 'error';
  onRunDiagnostic: () => void;
}

export const Header: React.FC<HeaderProps> = ({ systemStatus, onRunDiagnostic }) => {
  const getStatusIcon = () => {
    switch (systemStatus) {
      case 'online':
        return <Wifi size={16} color="#00ff88" />;
      case 'offline':
        return <Wifi size={16} color="#ff4444" />;
      case 'error':
        return <AlertCircle size={16} color="#ffaa00" />;
      default:
        return <Wifi size={16} color="#666" />;
    }
  };

  const getStatusText = () => {
    switch (systemStatus) {
      case 'online':
        return 'System Online';
      case 'offline':
        return 'System Offline';
      case 'error':
        return 'System Error';
      default:
        return 'Unknown Status';
    }
  };

  return (
    <header style={{
      background: 'linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%)',
      borderBottom: '1px solid #333',
      padding: '16px 20px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '8px 12px',
          background: 'rgba(0, 255, 136, 0.1)',
          borderRadius: '6px',
          border: '1px solid rgba(0, 255, 136, 0.3)'
        }}>
          <Zap size={20} color="#00ff88" />
          <h1 style={{
            margin: 0,
            fontSize: '1.5rem',
            fontWeight: '700',
            background: 'linear-gradient(45deg, #00ff88, #00aaff)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text'
          }}>
            ULTRON AGENT
          </h1>
        </div>
        
        <div style={{
          fontSize: '0.8rem',
          color: '#666',
          fontFamily: 'monospace'
        }}>
          v2.0.1 | Advanced AI Assistant Interface
        </div>
      </div>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <button
          className="button"
          onClick={onRunDiagnostic}
          style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
        >
          <Shield size={14} />
          Run Diagnostic
        </button>
        
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 12px',
          background: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '4px',
          fontSize: '0.8rem'
        }}>
          {getStatusIcon()}
          <span style={{
            color: systemStatus === 'online' ? '#00ff88' : 
                   systemStatus === 'offline' ? '#ff4444' : '#ffaa00'
          }}>
            {getStatusText()}
          </span>
        </div>
        
        <div style={{
          fontSize: '0.8rem',
          color: '#999',
          fontFamily: 'monospace'
        }}>
          {new Date().toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
          })}
        </div>
      </div>
    </header>
  );
};

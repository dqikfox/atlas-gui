import React from 'react';
import { Activity } from 'lucide-react';
import { ActivityLog } from '../types';

interface ActivityLogPanelProps {
  logs: ActivityLog[];
  logsEndRef: React.RefObject<HTMLDivElement>;
  onClearLogs: () => void;
}

/**
 * Activity Log Panel Component - FIXED for proper chronological ordering
 */
export const ActivityLogPanel: React.FC<ActivityLogPanelProps> = ({
  logs,
  logsEndRef,
  onClearLogs
}) => {
  const formatTime = (timestamp: Date) => {
    return timestamp.toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const getLogTypeColor = (type: ActivityLog['type']) => {
    switch (type) {
      case 'user':
        return '#00aaff';
      case 'ai':
        return '#00ff88';
      case 'system':
        return '#ffaa00';
      default:
        return '#cccccc';
    }
  };

  const getLogTypeIcon = (type: ActivityLog['type']) => {
    switch (type) {
      case 'user':
        return '👤';
      case 'ai':
        return '🤖';
      case 'system':
        return '⚙️';
      default:
        return '📝';
    }
  };

  return (
    <div className="panel">
      <div className="panel-header">
        <h3 className="panel-title">
          <Activity size={20} />
          Activity Log
        </h3>
        <button className="button" onClick={onClearLogs}>
          Clear
        </button>
      </div>
      
      <div className="panel-content">
        <div className="scrollable" style={{ height: '100%' }}>
          {logs.length === 0 ? (
            <div style={{ 
              color: '#666', 
              textAlign: 'center', 
              padding: '20px',
              fontStyle: 'italic'
            }}>
              No activity logs yet...
            </div>
          ) : (
            // CRITICAL FIX: Display logs in natural order (oldest to newest)
            // The logs array is already properly ordered from the hook
            logs.map((log) => (
              <div
                key={log.id}
                className="fade-in"
                style={{
                  padding: '12px',
                  marginBottom: '8px',
                  background: 'rgba(255, 255, 255, 0.05)',
                  borderRadius: '6px',
                  borderLeft: `3px solid ${getLogTypeColor(log.type)}`,
                  fontSize: '0.9rem',
                  lineHeight: '1.4'
                }}
              >
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  marginBottom: '4px'
                }}>
                  <span>{getLogTypeIcon(log.type)}</span>
                  <span style={{
                    color: getLogTypeColor(log.type),
                    fontWeight: '600',
                    textTransform: 'uppercase',
                    fontSize: '0.8rem'
                  }}>
                    {log.type}
                  </span>
                  <span style={{
                    color: '#999',
                    fontSize: '0.8rem'
                  }}>
                    {formatTime(log.timestamp)}
                  </span>
                  {log.provider && (
                    <span style={{
                      color: '#666',
                      fontSize: '0.8rem',
                      background: 'rgba(255, 255, 255, 0.1)',
                      padding: '2px 6px',
                      borderRadius: '3px'
                    }}>
                      {log.provider}/{log.model}
                    </span>
                  )}
                </div>
                <div style={{ color: '#ddd' }}>
                  {log.message}
                </div>
              </div>
            ))
          )}
          
          {/* CRITICAL: Scroll anchor for auto-scroll to bottom */}
          <div ref={logsEndRef} style={{ height: '1px' }} />
        </div>
      </div>
    </div>
  );
};

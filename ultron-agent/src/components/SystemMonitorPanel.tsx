import React from 'react';
import { Monitor, Cpu, HardDrive, MemoryStick } from 'lucide-react';
import { SystemMetrics } from '../types';

interface SystemMonitorPanelProps {
  metrics: SystemMetrics;
}

export const SystemMonitorPanel: React.FC<SystemMonitorPanelProps> = ({ metrics }) => {
  const getUsageColor = (usage: number) => {
    if (usage < 50) return '#00ff88';
    if (usage < 80) return '#ffaa00';
    return '#ff4444';
  };

  const MetricBar: React.FC<{ label: string; value: number; icon: React.ReactNode }> = ({ 
    label, 
    value, 
    icon 
  }) => (
    <div style={{ marginBottom: '16px' }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '6px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {icon}
          <span style={{ fontSize: '0.9rem', fontWeight: '500' }}>{label}</span>
        </div>
        <span style={{
          fontSize: '0.8rem',
          color: getUsageColor(value),
          fontWeight: '600'
        }}>
          {value}%
        </span>
      </div>
      <div style={{
        width: '100%',
        height: '8px',
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '4px',
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${value}%`,
          height: '100%',
          background: getUsageColor(value),
          borderRadius: '4px',
          transition: 'all 0.3s ease'
        }} />
      </div>
    </div>
  );

  return (
    <div className="panel">
      <div className="panel-header">
        <h3 className="panel-title">
          <Monitor size={20} />
          System Monitor
        </h3>
        <div className="status-indicator status-online" />
      </div>
      
      <div className="panel-content">
        <MetricBar
          label="CPU Usage"
          value={metrics.cpu}
          icon={<Cpu size={16} color={getUsageColor(metrics.cpu)} />}
        />
        
        <MetricBar
          label="Memory Usage"
          value={metrics.memory}
          icon={<MemoryStick size={16} color={getUsageColor(metrics.memory)} />}
        />
        
        <MetricBar
          label="Disk Usage"
          value={metrics.disk}
          icon={<HardDrive size={16} color={getUsageColor(metrics.disk)} />}
        />
        
        <div style={{
          marginTop: '20px',
          padding: '12px',
          background: 'rgba(0, 255, 136, 0.1)',
          borderRadius: '6px',
          fontSize: '0.8rem',
          color: '#00ff88'
        }}>
          ℹ️ System is running optimally
        </div>
      </div>
    </div>
  );
};

import { useState, useEffect } from 'react';
import { SystemMetrics } from '../types';

/**
 * Hook to monitor system metrics (simulated for demo)
 */
export const useSystemMetrics = () => {
  const [metrics, setMetrics] = useState<SystemMetrics>({
    cpu: 0,
    memory: 0,
    disk: 0
  });

  useEffect(() => {
    // Simulate system metrics updates
    const interval = setInterval(() => {
      setMetrics({
        cpu: Math.floor(Math.random() * 100),
        memory: Math.floor(Math.random() * 100),
        disk: Math.floor(Math.random() * 100)
      });
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return metrics;
};

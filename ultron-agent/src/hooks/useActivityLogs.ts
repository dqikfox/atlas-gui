import { useState, useCallback, useEffect, useRef } from 'react';
import { ActivityLog } from '../types';

/**
 * Hook to manage activity logs with proper chronological ordering
 * FIX: Ensures new messages appear at the bottom (latest at end of array)
 */
export const useActivityLogs = () => {
  const [logs, setLogs] = useState<ActivityLog[]>([]);
  const logsEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new logs are added
  const scrollToBottom = useCallback(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  // Add a new log entry - FIXED: append to end for chronological order
  const addLog = useCallback((log: Omit<ActivityLog, 'id' | 'timestamp'>) => {
    const newLog: ActivityLog = {
      ...log,
      id: `log_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date(),
    };

    setLogs((prevLogs) => {
      // CRITICAL FIX: Append new log to END of array (not beginning)
      // This ensures chronological order: oldest first, newest last
      const newLogs = [...prevLogs, newLog];
      
      // Keep only last 100 logs for performance
      if (newLogs.length > 100) {
        return newLogs.slice(-100);
      }
      
      return newLogs;
    });
  }, []);

  // Clear all logs
  const clearLogs = useCallback(() => {
    setLogs([]);
  }, []);

  // Auto-scroll to bottom when logs change
  useEffect(() => {
    const timeoutId = setTimeout(scrollToBottom, 100);
    return () => clearTimeout(timeoutId);
  }, [logs, scrollToBottom]);

  // Add initial system log
  useEffect(() => {
    addLog({
      type: 'system',
      message: 'Ultron Agent initialized successfully'
    });
  }, [addLog]);

  return {
    logs,
    addLog,
    clearLogs,
    logsEndRef,
    scrollToBottom
  };
};

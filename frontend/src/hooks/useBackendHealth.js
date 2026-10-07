import { useState, useEffect, useCallback } from 'react';
import { getBackendHealth } from '../api/api';

/**
 * Custom React hook to check and monitor CareerIQ FastAPI backend health.
 *
 * Visual states:
 * - 'connecting': Initial status on load / during check
 * - 'connected': Backend is healthy and reachable (HTTP 200)
 * - 'offline': Backend is unreachable or returned an error
 *
 * @param {Object} options
 * @param {number} [options.pollInterval=5000] - Polling interval in ms (default 5000ms)
 * @returns {{
 *   status: 'connecting' | 'connected' | 'offline',
 *   data: { status: string, service: string } | null,
 *   error: Error | null,
 *   checkHealth: () => Promise<void>
 * }}
 */
export function useBackendHealth({ pollInterval = 5000 } = {}) {
  const [status, setStatus] = useState('connecting');
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const checkHealth = useCallback(async () => {
    try {
      const result = await getBackendHealth();
      setData(result);
      setError(null);
      setStatus('connected');
    } catch (err) {
      console.error('[CareerIQ] Backend health check failed:', err);
      setError(err);
      setData(null);
      setStatus('offline');
    }
  }, []);

  useEffect(() => {
    let isMounted = true;

    const performCheck = async () => {
      if (!isMounted) return;
      await checkHealth();
    };

    // Immediate check on mount
    performCheck();

    // Periodic check to seamlessly detect offline / online transitions
    let intervalId = null;
    if (pollInterval > 0) {
      intervalId = setInterval(performCheck, pollInterval);
    }

    return () => {
      isMounted = false;
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [checkHealth, pollInterval]);

  return { status, data, error, checkHealth };
}

import { useCallback, useEffect, useState } from 'react';

export function useAsyncData(loader) {
  const [state, setState] = useState({ data: null, loading: true, error: null });

  const run = useCallback(async () => {
    setState({ data: null, loading: true, error: null });
    try {
      const data = await loader();
      setState({ data, loading: false, error: null });
    } catch (error) {
      setState({ data: null, loading: false, error });
    }
  }, [loader]);

  useEffect(() => {
    run();
  }, [run]);

  return { ...state, retry: run };
}

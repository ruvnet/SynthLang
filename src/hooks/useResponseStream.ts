import { useState } from 'react';
import { openRouterService } from '../services/openRouterService';

interface StreamOptions {
  model: string;
  messages: Array<{
    role: string;
    content: string;
  }>;
  apiKey: string;
  stream?: boolean;
  temperature?: number;
  max_tokens?: number;
  onChunk?: (chunk: string) => void;
}

export const useResponseStream = () => {
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startStream = async (options: StreamOptions) => {
    setIsStreaming(true);
    setError(null);

    try {
      const { apiKey, ...streamOptions } = options;
      const response = await openRouterService.streamCompletion({
        ...streamOptions,
        stream: true,
        onChunk: options.onChunk
      }, apiKey);
      return response;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to stream response');
      throw err;
    } finally {
      setIsStreaming(false);
    }
  };

  return {
    startStream,
    isStreaming,
    error
  };
};

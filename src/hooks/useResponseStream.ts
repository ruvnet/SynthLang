import { useState, useCallback } from 'react';
import { SynthLangConfig } from '../components/AdvancedCalculator/types';

interface ResponseState {
  isStreaming: boolean;
  response: string;
  isComplete: boolean;
}

export function useResponseStream(config: SynthLangConfig) {
  const [state, setState] = useState<ResponseState>({
    isStreaming: false,
    response: '',
    isComplete: false
  });

  const generateResponse = useCallback(() => {
    // Generate response based on enabled frameworks and settings
    const frameworks = Object.entries(config.frameworks)
      .filter(([_, state]) => state.enabled)
      .map(([id, state]) => ({
        id,
        glyphs: state.selectedGlyphs
      }));

    const responseLines = [
      '{\n  "analysis": {',
      '    "frameworks": {',
      ...frameworks.map(f => `      "${f.id}": {\n        "glyphs": [${f.glyphs.map(g => `"${g}"`).join(', ')}]\n      }`),
      '    },',
      '    "optimizations": {',
      ...Object.entries(config.optimizations).map(([key, value]) => `      "${key}": ${value}`),
      '    },',
      '    "features": {',
      ...Object.entries(config.features).map(([key, value]) => {
        if (typeof value === 'string') {
          return `      "${key}": "${value}"`;
        }
        return `      "${key}": ${value}`;
      }),
      '    }',
      '  },',
      '  "result": {',
      '    "model": "' + config.model + '",',
      '    "contextSize": ' + config.contextSize + ',',
      '    "status": "success",',
      '    "timestamp": "' + new Date().toISOString() + '"',
      '  }',
      '}'
    ];

    return responseLines.join('\n');
  }, [config]);

  const startStream = useCallback(() => {
    if (state.isStreaming) return;

    const fullResponse = generateResponse();
    let currentIndex = 0;

    setState(prev => ({ ...prev, isStreaming: true, response: '', isComplete: false }));

    const interval = setInterval(() => {
      if (currentIndex >= fullResponse.length) {
        clearInterval(interval);
        setState(prev => ({ ...prev, isStreaming: false, isComplete: true }));
        return;
      }

      setState(prev => ({
        ...prev,
        response: fullResponse.slice(0, currentIndex + 1)
      }));

      currentIndex++;
    }, 10); // Stream characters at 10ms intervals

    return () => clearInterval(interval);
  }, [state.isStreaming, generateResponse]);

  const resetStream = useCallback(() => {
    setState({
      isStreaming: false,
      response: '',
      isComplete: false
    });
  }, []);

  return {
    response: state.response,
    isStreaming: state.isStreaming,
    isComplete: state.isComplete,
    startStream,
    resetStream
  };
}

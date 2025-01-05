import { createContext, useContext, ReactNode, useCallback, useState } from 'react';
import { usePlayground } from './usePlayground';

interface PlaygroundState {
  code: string;
  copied: boolean;
  output: string | null;
  errors: string[];
  highlightedCode: string;
  isLoading: boolean;
}

interface PlaygroundContextType extends PlaygroundState {
  setCode: (code: string) => void;
  handleCopy: () => Promise<void>;
  handleRun: () => void;
  handleReset: () => void;
  handleKeyDown: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  loadExample: (code: string) => void;
}

const PlaygroundContext = createContext<PlaygroundContextType | null>(null);

interface PlaygroundProviderProps {
  children: ReactNode;
  initialCode: string;
  onRun?: (code: string) => void;
}

export const PlaygroundProvider = ({
  children,
  initialCode,
  onRun
}: PlaygroundProviderProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const playground = usePlayground({ 
    initialCode,
    onRun: onRun ? async (code) => {
      try {
        setIsLoading(true);
        await onRun(code);
      } finally {
        setIsLoading(false);
      }
    } : undefined
  });

  // Wrap loadExample to handle loading state
  const handleLoadExample = useCallback(async (code: string) => {
    try {
      setIsLoading(true);
      playground.loadExample(code);
    } finally {
      setIsLoading(false);
    }
  }, [playground]);

  const value: PlaygroundContextType = {
    ...playground,
    isLoading,
    loadExample: handleLoadExample
  };

  return (
    <PlaygroundContext.Provider value={value}>
      {children}
    </PlaygroundContext.Provider>
  );
};

export const usePlaygroundContext = () => {
  const context = useContext(PlaygroundContext);
  if (!context) {
    throw new Error('usePlaygroundContext must be used within a PlaygroundProvider');
  }
  return context;
};

// Helper components for the playground
export const PlaygroundError = ({ 
  error 
}: { 
  error: string;
}) => (
  <div className="flex items-center gap-2 text-red-400 text-sm">
    <span className="text-red-400/60">•</span>
    <span>{error}</span>
  </div>
);

export const PlaygroundOutput = ({ 
  children 
}: { 
  children: ReactNode;
}) => (
  <pre className="font-mono text-sm text-muted-foreground whitespace-pre-wrap 
                  bg-black/10 p-4 rounded-lg">
    {children}
  </pre>
);

export const PlaygroundLoading = () => (
  <div className="flex items-center justify-center p-4">
    <div className="animate-spin rounded-full h-6 w-6 border-2 border-purple-500 border-t-transparent" />
  </div>
);

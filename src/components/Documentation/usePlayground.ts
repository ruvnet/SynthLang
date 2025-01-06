import { useState, useEffect, useCallback } from 'react';
import { useSynthLang } from './useSynthLang';
import type { PlaygroundSettings } from './PlaygroundSettings';
import { useSettingsContext } from '../../services/settingsService';
import { callOpenRouter, SYSTEM_PROMPT } from '../../services/openRouterService';

interface UsePlaygroundProps {
  initialCode: string;
  onRun?: (code: string) => void;
}

export const usePlayground = ({ initialCode, onRun }: UsePlaygroundProps) => {
  const [code, setCode] = useState(initialCode);
  const [copied, setCopied] = useState(false);
  const [output, setOutput] = useState<string | null>(null);
  const [errors, setErrors] = useState<string[]>([]);
  const [highlightedCode, setHighlightedCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { settings: globalSettings } = useSettingsContext();
  const [settings, setSettings] = useState<PlaygroundSettings>({
    model: "gpt-4",
    temperature: 0.7,
    maxTokens: 1000,
    autoFormat: true,
    syntaxHighlighting: true,
    showLineNumbers: true,
    systemPrompt: SYSTEM_PROMPT.interpreter
  });

  const { executeSynthLang, validateSynthLang, highlightSyntax } = useSynthLang();

  // Update syntax highlighting when code changes
  useEffect(() => {
    if (settings.syntaxHighlighting) {
      setHighlightedCode(highlightSyntax(code));
    } else {
      setHighlightedCode(code);
    }
  }, [code, highlightSyntax, settings.syntaxHighlighting]);

  const setCodeWithValidation = useCallback((newCode: string) => {
    setCode(newCode);
    setErrors([]);
    setOutput(null);
  }, []);

  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy code:', error);
    }
  }, [code]);

  const handleRun = useCallback(async () => {
    try {
      setIsLoading(true);
      setErrors([]);
      setOutput("");

      // Skip validation for comment-only code
      const nonCommentLines = code.split('\n')
        .map(line => line.trim())
        .filter(line => line && !line.startsWith('#'));

      if (nonCommentLines.length > 0) {
        const validationErrors = validateSynthLang(code);
        if (validationErrors.length > 0) {
          setErrors(validationErrors);
          setIsLoading(false);
          return;
        }
      }

      if (onRun) {
        await onRun(code);
      } else if (globalSettings?.openRouterApiKey) {
        try {
          await callOpenRouter(
            code, 
            {
              model: settings.model,
              temperature: settings.temperature,
              maxTokens: settings.maxTokens
            }, 
            globalSettings.openRouterApiKey,
            'interpreter',
            undefined,
            undefined,
            (chunk) => {
              setOutput(prev => (prev || "") + chunk);
            }
          );
        } catch (error) {
          setErrors([error instanceof Error ? error.message : 'Failed to process code']);
        }
      } else {
        const result = executeSynthLang(code);
        if (result.error) {
          setErrors([result.error]);
        } else {
          setOutput(result.output);
        }
      }
    } catch (error) {
      setErrors([error instanceof Error ? error.message : 'An error occurred']);
    } finally {
      setIsLoading(false);
    }
  }, [code, onRun, executeSynthLang, validateSynthLang, settings, globalSettings?.openRouterApiKey]);

  const handleReset = useCallback(() => {
    setCode(initialCode);
    setOutput(null);
    setErrors([]);
  }, [initialCode]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const target = e.currentTarget;
      const start = target.selectionStart;
      const end = target.selectionEnd;
      const newCode = code.substring(0, start) + '  ' + code.substring(end);
      
      setCode(newCode);
      
      // Set cursor position after the inserted spaces
      requestAnimationFrame(() => {
        target.selectionStart = target.selectionEnd = start + 2;
      });
    } else if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      handleRun();
    } else if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === 'R') {
      e.preventDefault();
      handleReset();
    }
  }, [code, handleRun, handleReset]);

  const loadExample = useCallback((exampleCode: string) => {
    setCode(exampleCode);
    setOutput(null);
    setErrors([]);
  }, []);

  const updateSettings = useCallback((newSettings: PlaygroundSettings) => {
    setSettings(newSettings);
  }, []);

  return {
    code,
    copied,
    output,
    errors,
    highlightedCode,
    isLoading,
    settings,
    setCode: setCodeWithValidation,
    handleCopy,
    handleRun,
    handleReset,
    handleKeyDown,
    loadExample,
    updateSettings
  };
};

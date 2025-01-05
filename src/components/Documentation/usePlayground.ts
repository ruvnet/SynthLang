import { useState, useEffect, useCallback } from 'react';
import { useSynthLang } from './useSynthLang';

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

  const { executeSynthLang, validateSynthLang, highlightSyntax } = useSynthLang();

  // Update syntax highlighting when code changes
  useEffect(() => {
    setHighlightedCode(highlightSyntax(code));
  }, [code, highlightSyntax]);

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

  const handleRun = useCallback(() => {
    try {
      // Skip validation for comment-only code
      const nonCommentLines = code.split('\n')
        .map(line => line.trim())
        .filter(line => line && !line.startsWith('#'));

      if (nonCommentLines.length > 0) {
        const validationErrors = validateSynthLang(code);
        setErrors(validationErrors);

        if (validationErrors.length === 0) {
          if (onRun) {
            onRun(code);
          } else {
            const result = executeSynthLang(code);
            if (result.error) {
              setErrors([result.error]);
              setOutput(null);
            } else {
              setOutput(result.output);
              setErrors([]);
            }
          }
        } else {
          setOutput(null);
        }
      } else {
        // For comment-only code, just show the formatted output
        const result = executeSynthLang(code);
        setOutput(result.output);
        setErrors([]);
      }
    } catch (error) {
      setErrors([error instanceof Error ? error.message : 'An error occurred']);
      setOutput(null);
    }
  }, [code, onRun, executeSynthLang, validateSynthLang]);

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
    try {
      setCode(exampleCode);
      setOutput(null);
      setErrors([]);

      // Automatically run the example if it's valid
      const nonCommentLines = exampleCode.split('\n')
        .map(line => line.trim())
        .filter(line => line && !line.startsWith('#'));

      if (nonCommentLines.length > 0) {
        const validationErrors = validateSynthLang(exampleCode);
        if (validationErrors.length === 0) {
          const result = executeSynthLang(exampleCode);
          if (!result.error) {
            setOutput(result.output);
          }
        }
      } else {
        // For comment-only code, just show the formatted output
        const result = executeSynthLang(exampleCode);
        setOutput(result.output);
      }
    } catch (error) {
      console.error('Failed to load example:', error);
    }
  }, [executeSynthLang, validateSynthLang]);

  return {
    code,
    copied,
    output,
    errors,
    highlightedCode,
    setCode: setCodeWithValidation,
    handleCopy,
    handleRun,
    handleReset,
    handleKeyDown,
    loadExample
  };
};

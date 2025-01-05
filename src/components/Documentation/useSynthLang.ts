import { useCallback } from 'react';

interface SynthLangResult {
  output: string;
  error?: string;
}

interface SynthLangOperation {
  type: 'input' | 'operation' | 'output' | 'control';
  content: string;
  modifiers?: string[];
}

export const useSynthLang = () => {
  const parseSynthLang = useCallback((code: string): SynthLangOperation[] => {
    const lines = code.split('\n').filter(line => line.trim());
    return lines.map(line => {
      const trimmed = line.trim();
      
      // Parse comments
      if (trimmed.startsWith('#')) {
        return {
          type: 'control',
          content: trimmed.slice(1).trim()
        };
      }

      // Extract modifiers
      const modifiers = trimmed.match(/(\^[a-zA-Z0-9_]+|@[a-zA-Z0-9_]+|\$[a-zA-Z0-9_]+|#[a-zA-Z0-9_]+)/g) || [];

      // Parse operations
      if (trimmed.startsWith('↹')) {
        return {
          type: 'input',
          content: trimmed.slice(1).trim(),
          modifiers
        };
      }
      if (trimmed.startsWith('⊕')) {
        return {
          type: 'operation',
          content: trimmed.slice(1).trim(),
          modifiers
        };
      }
      if (trimmed.startsWith('Σ')) {
        return {
          type: 'output',
          content: trimmed.slice(1).trim(),
          modifiers
        };
      }

      return {
        type: 'control',
        content: trimmed
      };
    });
  }, []);

  const executeSynthLang = useCallback((code: string): SynthLangResult => {
    try {
      const operations = parseSynthLang(code);
      
      // Format operations into readable output
      const output = operations.map(op => {
        const modifierStr = op.modifiers?.length 
          ? ` [${op.modifiers.join(', ')}]`
          : '';

        switch (op.type) {
          case 'input':
            return `Input: ${op.content}${modifierStr}`;
          case 'operation':
            return `Operation: ${op.content}${modifierStr}`;
          case 'output':
            return `Output: ${op.content}${modifierStr}`;
          case 'control':
            return `// ${op.content}`;
        }
      }).join('\n');

      return { output };
    } catch (error) {
      return {
        output: '',
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      };
    }
  }, [parseSynthLang]);

  const highlightSyntax = useCallback((code: string): string => {
    return code.replace(
      /(↹|⊕|Σ|→|∀|∃|⇒|↺|⊥|⊤|⊗|∩|∪|∆|≡|≠)|\b(try|catch|finally|case|when)\b|(@\w+|\$\w+|\^\w+|#\w+)|("[^"]*")|(\{[^}]*\})|(\[[^\]]*\])|#.*$/gm,
      (match, operator, keyword, modifier, string, object, array, comment) => {
        if (operator) return `<span class="text-purple-400">${operator}</span>`;
        if (keyword) return `<span class="text-blue-400">${keyword}</span>`;
        if (modifier) return `<span class="text-green-400">${modifier}</span>`;
        if (string) return `<span class="text-yellow-300">${string}</span>`;
        if (object || array) return `<span class="text-blue-300">${match}</span>`;
        if (comment) return `<span class="text-gray-500">${match}</span>`;
        return match;
      }
    );
  }, []);

  const validateSynthLang = useCallback((code: string): string[] => {
    const errors: string[] = [];
    const lines = code.split('\n');
    let hasInput = false;
    let hasOutput = false;
    let hasNonCommentLines = false;

    lines.forEach((line, index) => {
      const trimmed = line.trim();
      
      // Skip empty lines and comments
      if (!trimmed || trimmed.startsWith('#')) return;

      hasNonCommentLines = true;

      if (trimmed.startsWith('↹')) hasInput = true;
      if (trimmed.startsWith('Σ')) hasOutput = true;

      // Validate basic syntax - only check non-empty, non-comment lines
      if (!trimmed.match(/^(↹|⊕|Σ|#)/)) {
        errors.push(`Line ${index + 1}: Invalid operation - must start with ↹, ⊕, or Σ`);
      }

      // Validate modifiers
      const modifiers = trimmed.match(/(\^[a-zA-Z0-9_]+|@[a-zA-Z0-9_]+|\$[a-zA-Z0-9_]+|#[a-zA-Z0-9_]+)/g) || [];
      modifiers.forEach(mod => {
        if (!mod.match(/^[\^@$#][a-zA-Z0-9_]+$/)) {
          errors.push(`Line ${index + 1}: Invalid modifier format - ${mod}`);
        }
      });

      // Validate operation syntax
      if (trimmed.startsWith('⊕')) {
        // Check for valid operation syntax
        const operationParts = trimmed.slice(1).trim().split(/\s+/);
        if (operationParts.length < 1) {
          errors.push(`Line ${index + 1}: Operation requires a command`);
        }
      }
    });

    // Only check for input/output requirements if there are non-comment lines
    if (hasNonCommentLines) {
      if (!hasInput) errors.push('Missing input operation (↹)');
      if (!hasOutput) errors.push('Missing output operation (Σ)');
    }

    return errors;
  }, []);

  return {
    executeSynthLang,
    highlightSyntax,
    validateSynthLang,
    parseSynthLang
  };
};

import { useCallback } from 'react';
import { validateSynthLang } from './useSynthLangUtils';

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
    const lines = code.split('\n');
    const operations: SynthLangOperation[] = [];
    let inJsonBlock = false;
    let jsonContent: string[] = [];
    let inMultilineContent = false;
    let multilineBuffer = '';

    for (let i = 0; i < lines.length; i++) {
      const trimmed = lines[i].trim();
      
      // Skip empty lines
      if (!trimmed) continue;

      // Parse comments
      if (trimmed.startsWith('#')) {
        operations.push({
          type: 'control',
          content: trimmed.slice(1).trim()
        });
        continue;
      }

      // Handle JSON block state
      if (trimmed.startsWith('Σ {')) {
        inJsonBlock = true;
        jsonContent = [trimmed];
        continue;
      }

      if (inJsonBlock) {
        jsonContent.push(trimmed);
        if (trimmed === '}') {
          operations.push({
            type: 'output',
            content: jsonContent.join('\n'),
            modifiers: []
          });
          inJsonBlock = false;
        }
        continue;
      }

      // Handle multiline content
      if (inMultilineContent) {
        multilineBuffer += '\n' + trimmed;
        if (trimmed.endsWith('"')) {
          inMultilineContent = false;
          const match = multilineBuffer.match(/^([↹⊕Σ])\s+([a-zA-Z0-9_]+)\s+"([^"]*)"(?:\s+(\^[a-zA-Z0-9_]+(?:\s+\^[a-zA-Z0-9_]+)*)?)?$/);
          if (match) {
            const [_, glyph, label, content, modifiers] = match;
            operations.push({
              type: glyph === '↹' ? 'input' : 
                    glyph === '⊕' ? 'operation' : 
                    glyph === 'Σ' ? 'output' : 'control',
              content: `${label} "${content}"`,
              modifiers: modifiers ? modifiers.split(/\s+/) : []
            });
          }
        }
        continue;
      }

      // Check for start of multiline content
      if (trimmed.match(/^[↹⊕Σ]\s+[a-zA-Z0-9_]+\s+"[^"]*$/)) {
        inMultilineContent = true;
        multilineBuffer = trimmed;
        continue;
      }

      // Parse single line operations
      const match = trimmed.match(/^([↹⊕Σ])\s+([a-zA-Z0-9_]+)\s+"([^"]*)"(?:\s+(\^[a-zA-Z0-9_]+(?:\s+\^[a-zA-Z0-9_]+)*)?)?$/);
      if (match) {
        const [_, glyph, label, content, modifiers] = match;
        operations.push({
          type: glyph === '↹' ? 'input' : 
                glyph === '⊕' ? 'operation' : 
                glyph === 'Σ' ? 'output' : 'control',
          content: `${label} "${content}"`,
          modifiers: modifiers ? modifiers.split(/\s+/) : []
        });
      } else {
        operations.push({
          type: 'control',
          content: trimmed
        });
      }
    }

    return operations;
  }, []);

  const executeSynthLang = useCallback((code: string): SynthLangResult => {
    try {
      // Validate the code first
      const errors = validateSynthLang(code);
      if (errors.length > 0) {
        return {
          output: '',
          error: errors.join('\n')
        };
      }

      // Parse and execute if valid
      const operations = parseSynthLang(code);
      
      // Format operations into readable output
      const output = operations.map(op => {
        switch (op.type) {
          case 'input':
            return `Input Operation: ${op.content}`;
          case 'operation':
            return `Process Operation: ${op.content}`;
          case 'output':
            return `Output Operation: ${op.content}`;
          case 'control':
            return `// ${op.content}`;
          default:
            return op.content;
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
    const lines = code.split('\n');
    let inJson = false;
    let jsonContent = '';

    return lines.map(line => {
      const trimmed = line.trim();

      // Handle JSON blocks
      if (trimmed.startsWith('Σ {')) {
        inJson = true;
        jsonContent = trimmed;
        return `<span class="text-purple-400">Σ</span> <span class="text-blue-300">${trimmed.slice(1)}</span>`;
      }
      if (inJson) {
        jsonContent += '\n' + trimmed;
        if (trimmed.endsWith('}')) {
          inJson = false;
          return `<span class="text-blue-300">${trimmed}</span>`;
        }
        return `<span class="text-blue-300">${trimmed}</span>`;
      }

      // Handle JSON content lines
      const jsonLineMatch = trimmed.match(/^([a-zA-Z0-9_]+):\s+(\^[a-zA-Z0-9_]+)(?:\s*,\s*)?$/);
      if (jsonLineMatch) {
        const [_, key, modifier] = jsonLineMatch;
        return `<span class="text-blue-400">${key}</span>: <span class="text-green-400">${modifier}</span>${trimmed.endsWith(',') ? ',' : ''}`;
      }

      // Handle regular lines
      return line.replace(
        /(↹|⊕|Σ)|\b([a-zA-Z0-9_]+)\s+(?=")|("[^"]*")|(\^[a-zA-Z0-9_]+)|#.*$/g,
        (match, glyph, label, content, modifier, comment) => {
          if (glyph) return `<span class="text-purple-400">${glyph}</span>`;
          if (label) return `<span class="text-blue-400">${label}</span>`;
          if (content) return `<span class="text-yellow-300">${content}</span>`;
          if (modifier) return `<span class="text-green-400">${modifier}</span>`;
          if (comment) return `<span class="text-gray-500">${comment}</span>`;
          return match;
        }
      );
    }).join('\n');
  }, []);

  return {
    executeSynthLang,
    highlightSyntax,
    validateSynthLang,
    parseSynthLang
  };
};

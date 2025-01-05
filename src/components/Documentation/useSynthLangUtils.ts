export const validateSynthLang = (code: string): string[] => {
  const errors: string[] = [];
  const lines = code.split('\n');
  let hasInput = false;
  let hasOutput = false;
  let hasNonCommentLines = false;

  let inJsonBlock = false;
  let jsonBraceCount = 0;
  let jsonStartLine = 0;
  let inMultilineContent = false;
  let multilineStartLine = 0;
  let multilineBuffer = '';

  for (let i = 0; i < lines.length; i++) {
    const trimmed = lines[i].trim();
    
    // Skip empty lines and comments
    if (!trimmed || trimmed.startsWith('#')) continue;

    hasNonCommentLines = true;

    // Handle JSON block state
    if (trimmed.startsWith('Σ {') || trimmed.match(/^Σ\s+\w+\s*{/)) {
      inJsonBlock = true;
      jsonBraceCount = 1;
      hasOutput = true;
      jsonStartLine = i + 1;
      continue;
    }

    if (inJsonBlock) {
      // Count braces
      for (const char of trimmed) {
        if (char === '{') jsonBraceCount++;
        if (char === '}') jsonBraceCount--;
      }

      // Handle closing brace
      if (trimmed === '}') {
        if (jsonBraceCount === 0) {
          inJsonBlock = false;
        }
        continue;
      }

      // Skip case statements, arrow syntax, and special formats in JSON blocks
      if (trimmed.startsWith('case ') || 
          trimmed.includes('→') || 
          trimmed.includes('⇒') ||
          trimmed.includes('||')) {
        continue;
      }

      // Skip nested JSON blocks
      if (trimmed.includes('{') || trimmed.includes('}')) {
        continue;
      }

      // Validate JSON content lines
      const jsonLineRegex = /^[a-zA-Z0-9_]+:\s+(?:(?:json|markdown|dashboard|formatted)\s+)?\^[a-zA-Z0-9_]+(?:\s*,\s*)?$/;
      if (!jsonLineRegex.test(trimmed)) {
        errors.push(`Line ${i + 1}: Invalid JSON format - must be key: ^modifier or key: type ^modifier`);
      }
      continue;
    }

    if (trimmed.startsWith('↹')) hasInput = true;
    if (trimmed.startsWith('Σ')) hasOutput = true;

    // Handle multiline content
    if (inMultilineContent) {
      multilineBuffer += '\n' + trimmed;
      if (trimmed.endsWith('"')) {
        inMultilineContent = false;
        // Validate the complete multiline content
        const fullLine = multilineBuffer;
        const match = fullLine.match(/^([↹⊕Σ])\s+([a-zA-Z0-9_]+)\s*"([^"]*)"(?:\s+(?:@[a-zA-Z0-9_]+|\^[a-zA-Z0-9_]+|\[[^\]]+\]|\{[^}]+\}|\→\s*\w+|\⇒\s*\{[^}]+\}|\→|\⇒|\⊗|\≡|\||)*)*$/);
        if (!match) {
          errors.push(`Line ${multilineStartLine + 1}: Invalid format - must follow pattern: label "content" ^modifiers`);
        }
      }
      continue;
    }

    // Check for start of multiline content
    if (trimmed.match(/^[↹⊕Σ]\s+[a-zA-Z0-9_]+\s*"[^"]*$/)) {
      inMultilineContent = true;
      multilineBuffer = trimmed;
      multilineStartLine = i;
      continue;
    }

    // Validate basic syntax - only check non-empty, non-comment lines
    if (!trimmed.match(/^(↹|⊕|Σ|#)/)) {
      errors.push(`Line ${i + 1}: Invalid operation - must start with ↹, ⊕, or Σ`);
      continue;
    }

    // Check for invalid label format first
    const labelMatch = trimmed.match(/^[↹⊕Σ]\s+([a-zA-Z0-9_-]+)/);
    if (labelMatch && labelMatch[1].includes('-')) {
      errors.push(`Line ${i + 1}: Invalid label - must be single word without hyphens or spaces`);
      continue;
    }

    // Skip lines with special syntax
    if (trimmed.includes('[') || trimmed.includes('{') || trimmed.includes('→') || trimmed.includes('⇒') || trimmed.includes('⊗') || trimmed.includes('≡') || trimmed.includes('||')) {
      continue;
    }

    // Parse operations with new format, including arrows, annotations, and brackets
    const operationRegex = /^([↹⊕Σ])\s+([a-zA-Z0-9_]+)(?:\s*"([^"]*)")?(?:\s+(?:@[a-zA-Z0-9_]+|\^[a-zA-Z0-9_]+(?:\s+\^[a-zA-Z0-9_]+)*|\[[^\]]+\]|\{[^}]+\}|\→\s*\w+|\⇒\s*\{[^}]+\}|\→|\⇒|\⊗|\≡|\||)*)*$/;
    const match = trimmed.match(operationRegex);

    if (!match) {
      errors.push(`Line ${i + 1}: Invalid format - must follow pattern: label "content" ^modifiers`);
      continue;
    }

    // Only validate content and modifiers for standard operations
    if (match) {
      const [_, glyph, label, content] = match;

      // Content validation for input operations
      if (glyph === '↹' && content === '') {
        errors.push(`Line ${i + 1}: Content cannot be empty`);
      }
    }
  }

  // Check for unclosed JSON block
  if (inJsonBlock) {
    errors.push(`Line ${jsonStartLine}: Invalid JSON output format - missing closing brace`);
  }

  // Only check for input/output requirements if there are non-comment lines
  if (hasNonCommentLines) {
    if (!hasInput) errors.push('Missing input operation (↹)');
    if (!hasOutput) errors.push('Missing output operation (Σ)');
  }

  return errors;
};

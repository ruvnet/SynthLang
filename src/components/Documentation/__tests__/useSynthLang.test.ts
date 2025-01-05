import { validateSynthLang } from '../useSynthLangUtils';

describe('SynthLang', () => {
  describe('validateSynthLang', () => {
    test('validates basic text analysis example with no space', () => {
      const code = `# Basic text analysis example
↹ text"Analyze this text for sentiment and key points"
⊕ analyze_sentiment ^thorough
⊕ extract_key_points ^comprehensive
Σ {
  sentiment: ^brief,
  points: ^bullet_points,
  confidence: ^percentage
}`;
      const errors = validateSynthLang(code);
      expect(errors).toHaveLength(0);
    });

    test('validates arrow syntax', () => {
      const code = `↹ topic "AI in Healthcare" @industry_context
⊕ research → outline
⊕ generate_draft ^creative
Σ {
  content: ^formatted
}`;
      const errors = validateSynthLang(code);
      expect(errors).toHaveLength(0);
    });

    test('validates context annotations', () => {
      const code = `↹ data "market data" @industry_trends
⊕ analyze "trends" ^comprehensive
⊕ identify "patterns" ^detailed
Σ report {
  summary: ^brief
}`;
      const errors = validateSynthLang(code);
      expect(errors).toHaveLength(0);
    });

    test('validates bracket modifiers', () => {
      const code = `↹ market_analysis "renewable energy" @context
⊕ focus "solar and wind" ^comprehensive
⊕ analyze "tech and cost" ^detailed
Σ report ^analysis`;
      const errors = validateSynthLang(code);
      expect(errors).toHaveLength(0);
    });

    test('validates complex JSON blocks', () => {
      const code = `↹ text "content"
⊕ process "data" ^analyze
Σ {
  processed: json ^structured,
  summary: markdown ^brief,
  metrics: dashboard ^interactive
}`;
      const errors = validateSynthLang(code);
      expect(errors).toHaveLength(0);
    });

    test('validates empty content', () => {
      const code = `↹ text ""`;
      const errors = validateSynthLang(code);
      expect(errors).toContain('Line 1: Content cannot be empty');
    });

    test('validates missing input operation', () => {
      const code = `⊕ analyze "text"`;
      const errors = validateSynthLang(code);
      expect(errors).toContain('Missing input operation (↹)');
    });

    test('validates missing output operation', () => {
      const code = `↹ text "input"`;
      const errors = validateSynthLang(code);
      expect(errors).toContain('Missing output operation (Σ)');
    });

    test('validates invalid label format', () => {
      const code = `↹ invalid-label "content"`;
      const errors = validateSynthLang(code);
      expect(errors).toContain('Line 1: Invalid label - must be single word without hyphens or spaces');
    });

    test('validates invalid modifier format', () => {
      const code = `↹ text "content" invalid_modifier`;
      const errors = validateSynthLang(code);
      expect(errors).toContain('Line 1: Invalid format - must follow pattern: label "content" ^modifiers');
    });

    test('validates JSON output format', () => {
      const code = `↹ text "content"
Σ {
  key1: ^mod1,
  key2: ^mod2
}`;
      const errors = validateSynthLang(code);
      expect(errors).toHaveLength(0);
    });

    test('validates invalid JSON format', () => {
      const code = `↹ text "content"
Σ {
  invalid_format
  key: ^mod
}`;
      const errors = validateSynthLang(code);
      expect(errors).toContain('Line 3: Invalid JSON format - must be key: ^modifier or key: type ^modifier');
    });

    test('validates missing JSON closing brace', () => {
      const code = `↹ text "content"
Σ {
  key: ^mod`;
      const errors = validateSynthLang(code);
      expect(errors).toContain('Line 2: Invalid JSON output format - missing closing brace');
    });

    test('validates multiple modifiers', () => {
      const code = `↹ text "content" ^mod1 ^mod2 ^mod3
⊕ process "data" ^mod4 ^mod5
Σ {
  key: ^mod
}`;
      const errors = validateSynthLang(code);
      expect(errors).toHaveLength(0);
    });

    test('validates comments', () => {
      const code = `# This is a comment
↹ text "content"
# Another comment
Σ {
  key: ^mod
}`;
      const errors = validateSynthLang(code);
      expect(errors).toHaveLength(0);
    });
  });
});

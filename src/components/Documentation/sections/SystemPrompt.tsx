import { Terminal } from "lucide-react";
import { DocSection } from "../types";
import { CodeExample } from "../CodeExample";

const systemPromptExample = {
  title: "SynthLang System Prompt",
  description: "The complete system prompt for implementing SynthLang in LLM applications",
  language: "markdown",
  code: `[Overview]
SynthLang is a hyper-efficient prompt language for LLMs, using compact glyphs and logographic scripts to reduce token usage and mitigate bias. You will interpret and respond to SynthLang instructions according to these rules.

[Grammar and Syntax]
1. Task Glyphs (T)
   - Σ (Summarize)
   - ↹ (Focus/Filter)
   - ⊕ (Combine/Merge)
   - ? (Query/Clarify)
   - IF (Conditional)
   (Each glyph must be preserved as a single token.)

2. Subject Glyphs (S)
   Examples: •dataset, •salesData, 花 (flower), 山 (mountain)
   (Represent tasks or data objects to be processed.)

3. Modifiers (M)
   Examples: ^4, ^eng, ^urgent, ^7d, ^brief, etc.
   (Add nuance or scope to tasks, e.g., emphasis level, output language, or time range.)

4. Flow Glyphs (F)
   Examples: [p=5], ⊕
   (Set priority or combine tasks.)

5. Microparticles
   - : (Link labels to objects)
   - => (Implication/Result)
   - | (Logical OR)
   - + (Concatenate outputs)
   - -> (Action direction)

[Usage Rules]
A. Keep the glyphs intact.
B. If a prompt is unclear, ask for clarification.
C. Follow modifiers strictly (e.g., if ^10w is specified, limit summaries to ~10 words).

[Examples]
USER: ↹ [p=5] 法:"montagne" ⊕ Σ "意味" ^eng
MODEL: "Chinese: '山'. English summary: 'The mountain is beautiful in spring.'"

[Output Formatting]
- Minimal text or bullet points if needed.
- Provide rationale only if ^rationale is included.
- Use English only if ^eng is explicitly requested, otherwise honor the language context.

[Error Handling / Clarifications]
- If conflicting modifiers appear, address whichever has higher priority (p=5 > p=2).
- If no clear resolution, ask the user for clarification.`
};

const implementationExample = {
  title: "Implementation Example",
  description: "Example of using the system prompt in your LLM application",
  language: "typescript",
  code: `import { OpenAI } from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

const SYSTEM_PROMPT = \`${systemPromptExample.code}\`;

async function processSynthLang(input: string) {
  const response = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [
      {
        role: "system",
        content: SYSTEM_PROMPT
      },
      {
        role: "user",
        content: input
      }
    ],
    temperature: 0.7,
    max_tokens: 1000
  });

  return response.choices[0].message.content;
}`
};

const usageExample = {
  title: "Usage Example",
  description: "Example of using SynthLang with the system prompt",
  code: `# Input text analysis with language translation
↹ text "Analyze the sentiment and key themes" ^thorough
⊕ translate -> 日本語 ^formal
Σ {
  sentiment: ^brief,
  themes: ^bullet_points,
  translation: ^polished
}`
};

const modelBehaviorExample = {
  title: "Model Behavior Control",
  description: "Fine-grained control of model behavior through system prompt configuration",
  language: "markdown",
  code: `[Model Behavior Configuration]
1. Response Format Control
   - JSON: ^json -> structured data output
   - Markdown: ^md -> formatted documentation
   - Plain: ^text -> unformatted response
   - Custom: Define schema with {...}

2. Processing Modes
   - Deterministic: ^exact -> consistent outputs
   - Creative: ^creative -> varied responses
   - Analytical: ^analytical -> detailed analysis
   - Concise: ^brief -> minimal output

3. Error Handling
   - Strict: Report all issues
   - Permissive: Auto-correct minor issues
   - Interactive: Request clarification
   - Silent: Best-effort execution

4. Context Management
   - Memory: Track conversation state
   - Reset: Clear context on demand
   - Merge: Combine multiple contexts
   - Scope: Limit context window`
};

const optimizationExample = {
  title: "System Prompt Optimization",
  description: "Techniques for optimizing system prompt performance",
  language: "markdown",
  code: `[Optimization Strategies]
1. Token Efficiency
   - Use compact representations
   - Leverage unicode symbols
   - Minimize repetition
   - Cache common patterns

2. Response Shaping
   - Template-based outputs
   - Schema validation
   - Format enforcement
   - Consistency checks

3. Performance Tuning
   - Batch similar requests
   - Prioritize critical paths
   - Cache frequent patterns
   - Optimize context window

4. Quality Control
   - Validate outputs
   - Monitor accuracy
   - Track metrics
   - Auto-correction`
};

export const SystemPrompt: DocSection = {
  title: "System Prompt",
  icon: Terminal,
  content: [
    {
      title: "Overview",
      text: "The SynthLang system prompt provides LLMs with the necessary context and rules to interpret and execute SynthLang commands. This standardized prompt ensures consistent behavior across different LLM implementations.",
      example: "",
      component: () => <CodeExample {...systemPromptExample} />
    },
    {
      title: "Implementation",
      text: "Implement SynthLang in your application by including the system prompt in your LLM requests. Here's an example using the OpenAI API:",
      example: "",
      component: () => <CodeExample {...implementationExample} />
    },
    {
      title: "Usage",
      text: "Once implemented, you can use SynthLang commands to interact with the LLM in a structured and efficient way:",
      example: "",
      component: () => <CodeExample {...usageExample} />
    },
    {
      title: "Model Behavior Control",
      text: "Fine-tune model behavior and response characteristics through system prompt configuration:",
      example: "",
      component: () => <CodeExample {...modelBehaviorExample} />
    },
    {
      title: "Optimization Techniques",
      text: "Strategies for optimizing system prompt performance and efficiency:",
      example: "",
      component: () => <CodeExample {...optimizationExample} />
    }
  ]
};

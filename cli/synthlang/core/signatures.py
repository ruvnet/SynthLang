"""Signature definitions for SynthLang DSPy modules."""
from dspy.signatures import Signature
from dspy.signatures.field import InputField, OutputField

class TranslateSignature(Signature):
    """Signature for translating natural language to SynthLang format."""
    source = InputField(desc="Natural language prompt to translate")
    target = OutputField(desc="Translated prompt in SynthLang format")
    explanation = OutputField(desc="Explanation of the translation")

    def __init__(self):
        super().__init__()
        self.instructions = (
            "Convert input to concise SynthLang format using these rules:\n\n"
            "RULES:\n"
            "1. Use ONLY these symbols: ↹ (input), ⊕ (process), Σ (output)\n"
            "2. NO quotes, arrows, or descriptions\n"
            "3. Use • to join related items\n"
            "4. Use => for transformations\n"
            "5. Maximum 30 characters per line\n"
            "6. Use mathematical operators (+, >, <, ^)\n"
            "7. Break complex tasks into steps\n\n"
            "IMPORTANT: Keep translations extremely concise!\n\n"
            "GOOD EXAMPLES:\n"
            "↹ data•source\n"
            "⊕ condition>5 => action\n"
            "Σ result + log\n\n"
            "↹ input•stream, params\n"
            "⊕ transform => output\n"
            "⊕ Σ final^2 + cache\n\n"
            "↹ news•feed•google\n"
            "⊕ sentiment>0 => pos\n"
            "⊕ sentiment<0 => neg\n"
            "Σ trend + factors\n\n"
            "BAD EXAMPLES (TOO VERBOSE):\n"
            "↹ data:\"source\" -> Parse input\n"
            "⊕ process:\"condition\" -> Check value\n\n"
            "IMPORTANT: Your output MUST follow this exact format. Do not use quotes, arrows, or descriptions."
        )

class GenerateSignature(Signature):
    """Signature for system prompt generation."""
    task = InputField(desc="Task description")
    prompt = OutputField(desc="Generated system prompt")
    rationale = OutputField(desc="Design rationale")
    metadata = OutputField(desc="Additional metadata")

    def __init__(self):
        super().__init__()
        self.instructions = (
            "Generate a system prompt from a task description. "
            "Input: task description. "
            "Output: prompt, rationale, and metadata."
        )

class OptimizeSignature(Signature):
    """Signature for prompt optimization using DSPy techniques."""
    prompt = InputField(desc="Original prompt to optimize")
    optimized = OutputField(desc="Optimized prompt")
    improvements = OutputField(desc="List of improvements made")
    clarity_score = OutputField(desc="Clarity score (0-1)")
    specificity_score = OutputField(desc="Specificity score (0-1)")
    consistency_score = OutputField(desc="Consistency score (0-1)")

    def __init__(self):
        super().__init__()
        self.instructions = (
            "Optimize the given prompt following DSPy best practices:\n\n"
            "1. CLARITY:\n"
            "   - Remove ambiguous language\n"
            "   - Use precise, specific terms\n"
            "   - Break down complex instructions\n\n"
            "2. SPECIFICITY:\n"
            "   - Add concrete examples\n"
            "   - Define expected formats\n"
            "   - Specify constraints\n\n"
            "3. CONSISTENCY:\n"
            "   - Maintain consistent terminology\n"
            "   - Use uniform formatting\n"
            "   - Align with system goals\n\n"
            "4. SCORING:\n"
            "   - Clarity: Rate how clear and unambiguous (0-1)\n"
            "   - Specificity: Rate level of detail and precision (0-1)\n"
            "   - Consistency: Rate terminology and format consistency (0-1)\n\n"
            "Output the optimized prompt, list specific improvements made, "
            "and provide numerical scores for each metric."
        )

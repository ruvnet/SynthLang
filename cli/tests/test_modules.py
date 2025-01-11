"""Tests for DSPy module implementations."""
import pytest
import dspy

from synthlang.core.modules import (
    SynthLangModule,
    FrameworkTranslator,
    SystemPromptGenerator
)
from synthlang.config import Config

@pytest.fixture
def config():
    """Test configuration fixture."""
    return Config(
        openai_api_key="sk-test",
        model="gpt-4o-mini",  # Using required model
        environment="testing",
        log_level="INFO"
    )

@pytest.fixture
def lm(config):
    """Language model fixture."""
    return dspy.OpenAI(
        model=config.model,
        api_key=config.openai_api_key
    )

def test_synthlang_module_initialization(lm):
    """Test SynthLangModule initialization."""
    module = SynthLangModule(lm)
    assert module.lm == lm
    assert isinstance(module, dspy.Module)

def test_framework_translator(lm):
    """Test FrameworkTranslator module."""
    translator = FrameworkTranslator(lm)
    
    # Test translation signatures
    assert hasattr(translator, "translate")
    assert callable(translator.translate)
    
    # Test translation input validation
    with pytest.raises(ValueError):
        translator.translate("")  # Empty input
    
    with pytest.raises(ValueError):
        translator.translate("   ")  # Whitespace only

def test_system_prompt_generator(lm):
    """Test SystemPromptGenerator module."""
    generator = SystemPromptGenerator(lm)
    
    # Test generator signatures
    assert hasattr(generator, "generate")
    assert callable(generator.generate)
    
    # Test generator input validation
    with pytest.raises(ValueError):
        generator.generate("")  # Empty input
    
    with pytest.raises(ValueError):
        generator.generate("   ")  # Whitespace only

def test_framework_translation_format(lm):
    """Test framework translation output format."""
    translator = FrameworkTranslator(lm)
    
    test_input = """
    def process_data(data):
        filtered = filter(data)
        transformed = transform(filtered)
        return analyze(transformed)
    """
    
    # Test translation format
    translation = translator.translate(test_input)
    assert isinstance(translation, dict)
    assert "source" in translation
    assert "target" in translation
    
    # Verify SynthLang format rules
    target = translation["target"]
    lines = target.strip().split('\n')
    
    # Rule 1: Only allowed symbols
    allowed_symbols = {'↹', '⊕', 'Σ', '•', '=>', '+', '>', '<', '^'}
    for line in lines:
        symbols = set(c for c in line if not c.isalnum() and not c.isspace())
        assert symbols.issubset(allowed_symbols), f"Invalid symbols in line: {line}"
    
    # Rule 2: No quotes or descriptions
    assert '"' not in target and "'" not in target, "Contains quotes"
    assert ':' not in target, "Contains descriptions"
    
    # Rule 3: Proper use of • for joining
    assert '•' in target, "Missing item joining with •"
    
    # Rule 4: Proper use of => for transformations
    assert '=>' in target, "Missing transformations with =>"
    
    # Rule 5: Line length limit
    assert all(len(line) <= 30 for line in lines), "Line exceeds 30 characters"
    
    # Rule 6: Mathematical operators
    assert any(op in target for op in ['+', '>', '<', '^']), "Missing mathematical operators"
    
    # Rule 7: Multiple steps (at least input, process, output)
    assert '↹' in target, "Missing input symbol"
    assert '⊕' in target, "Missing process symbol"
    assert 'Σ' in target, "Missing output symbol"

def test_framework_translation_examples(lm):
    """Test framework translation with specific examples."""
    translator = FrameworkTranslator(lm)
    
    test_cases = [
        {
            "input": "Filter data where value > 5, transform results, and calculate sum",
            "expected_output": [
                "↹ data•value",
                "⊕ value>5 => filter",
                "⊕ filter => transform",
                "Σ transform + sum"
            ]
        },
        {
            "input": "Process stream of events, aggregate by type, output trends",
            "expected_output": [
                "↹ events•stream",
                "⊕ type => aggregate",
                "Σ trends^2"
            ]
        },
        {
            "input": "Analyze sentiment from multiple sources and generate report",
            "expected_output": [
                "↹ sources•sentiment",
                "⊕ sentiment>0 => pos",
                "⊕ sentiment<0 => neg",
                "Σ report + trends"
            ]
        }
    ]
    
    for case in test_cases:
        translation = translator.translate(case["input"])
        result_lines = translation["target"].strip().split('\n')
        
        # Verify format matches expected output
        assert len(result_lines) == len(case["expected_output"]), \
            f"Expected {len(case['expected_output'])} lines, got {len(result_lines)}"
        
        for actual, expected in zip(result_lines, case["expected_output"]):
            # Verify line structure
            assert actual.startswith(expected[0]), \
                f"Line should start with {expected[0]}"
            
            # Verify line length
            assert len(actual) <= 30, \
                f"Line exceeds 30 characters: {actual}"
            
            # Verify proper symbol usage
            if '↹' in expected:
                assert '•' in actual, "Input line missing item separator"
        for section in case["expected_sections"]:
            assert section in prompt["prompt"], f"Missing section {section} in prompt"

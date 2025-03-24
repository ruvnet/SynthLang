"""Tests for DSPy module implementations."""
import pytest
import dspy
from unittest.mock import Mock

from synthlang.core.base import SynthLangModule
from synthlang.core.translator import FrameworkTranslator
from synthlang.core.generator import SystemPromptGenerator
from synthlang.core.types import SynthLangSymbols, FormatRules
from synthlang.config import Config

@pytest.fixture
def config():
    """Test configuration fixture."""
    return Config(
        openai_api_key="sk-test",
        model="gpt-4o-mini",
        environment="testing",
        log_level="INFO"
    )

@pytest.fixture
def mock_api_response():
    """Mock raw API response."""
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677858242,
        "model": "gpt-4o-mini",
        "usage": {
            "prompt_tokens": 56,
            "completion_tokens": 31,
            "total_tokens": 87
        },
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Test response content"
                },
                "finish_reason": "stop",
                "index": 0
            }
        ]
    }

@pytest.fixture
def mock_translation_response(mock_api_response):
    """Mock translation API response."""
    mock_api_response["choices"][0]["message"]["content"] = {
        "source": "def process_data(data):\n    filtered = filter(data)\n    transformed = transform(filtered)\n    return analyze(transformed)",
        "target": f"{SynthLangSymbols.INPUT} data{SynthLangSymbols.JOIN}process\n"
                 f"{SynthLangSymbols.PROCESS} data {SynthLangSymbols.TRANSFORM} filter\n"
                 f"{SynthLangSymbols.PROCESS} filtered {SynthLangSymbols.TRANSFORM} transform\n"
                 f"{SynthLangSymbols.OUTPUT} analyze(transformed)"
    }
    return mock_api_response

@pytest.fixture
def mock_generator_response(mock_api_response):
    """Mock system prompt generator API response."""
    mock_api_response["choices"][0]["message"]["content"] = {
        "prompt": "You are a helpful recipe chatbot assistant that specializes in finding and suggesting recipes based on user preferences and dietary restrictions.",
        "rationale": "This prompt establishes the chatbot's role as a recipe specialist while emphasizing its ability to consider user preferences and restrictions.",
        "metadata": {
            "model": "gpt-4o-mini",
            "timestamp": "2025-01-11T12:00:00Z",
            "version": "1.0",
            "domain": "cooking",
            "capabilities": ["recipe_search", "dietary_restrictions", "ingredient_substitution"]
        }
    }
    return mock_api_response

@pytest.fixture
def mock_lm():
    """Mock language model client."""
    mock = Mock()
    mock.api_key = "sk-test"
    mock.model = "gpt-4o-mini"
    mock.generate = Mock()
    return mock

def test_synthlang_module_initialization(config, mock_lm):
    """Test SynthLangModule initialization."""
    module = SynthLangModule(lm=mock_lm)
    assert module.lm == mock_lm
    assert module.lm.api_key == config.openai_api_key
    assert module.lm.model == config.model

def test_framework_translator(config, mock_lm, mock_translation_response):
    """Test FrameworkTranslator module."""
    mock_lm.generate.return_value = mock_translation_response
    
    translator = FrameworkTranslator(lm=mock_lm)
    
    # Test translation signatures
    assert hasattr(translator, "translate")
    assert callable(translator.translate)
    
    # Test translation input validation
    with pytest.raises(ValueError):
        translator.translate("")  # Empty input
    
    with pytest.raises(ValueError):
        translator.translate("   ")  # Whitespace only
        
    # Test successful translation
    result = translator.translate("def process_data(data):")
    assert result == mock_translation_response

def test_system_prompt_generator(config, mock_lm, mock_generator_response):
    """Test SystemPromptGenerator module."""
    mock_lm.generate.return_value = mock_generator_response
    
    generator = SystemPromptGenerator(lm=mock_lm)
    
    # Test generator signatures
    assert hasattr(generator, "generate")
    assert callable(generator.generate)
    
    # Test generator input validation
    with pytest.raises(ValueError):
        generator.generate("")  # Empty input
    
    with pytest.raises(ValueError):
        generator.generate("   ")  # Whitespace only
        
    # Test generation output format
    test_input = "create a chatbot that helps users find recipes"
    result = generator.generate(test_input)
    
    # Verify result matches mock response
    assert result == mock_generator_response
    
    # Verify structure
    assert isinstance(result, dict)
    assert "prompt" in result
    assert "rationale" in result
    assert "metadata" in result
    assert result["metadata"]["model"] == config.model

def test_framework_translation_format(config):
    """Test framework translation output format."""
    lm = dspy.LM(model=config.model, api_key=config.openai_api_key)
    translator = FrameworkTranslator(lm=lm)
    
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
    for line in lines:
        symbols = set(c for c in line if not c.isalnum() and not c.isspace())
        assert symbols.issubset(FormatRules.ALLOWED_SYMBOLS), f"Invalid symbols in line: {line}"
    
    # Rule 2: No quotes or descriptions
    assert '"' not in target and "'" not in target, "Contains quotes"
    assert ':' not in target, "Contains descriptions"
    
    # Rule 3: Proper use of • for joining
    assert SynthLangSymbols.JOIN in target, "Missing item joining with •"
    
    # Rule 4: Proper use of => for transformations
    assert SynthLangSymbols.TRANSFORM in target, "Missing transformations with =>"
    
    # Rule 5: Line length limit
    assert all(len(line) <= FormatRules.MAX_LINE_LENGTH for line in lines), "Line exceeds length limit"
    
    # Rule 6: Mathematical operators
    assert any(op in target for op in SynthLangSymbols.OPERATORS), "Missing mathematical operators"
    
    # Rule 7: Multiple steps (at least input, process, output)
    assert SynthLangSymbols.INPUT in target, "Missing input symbol"
    assert SynthLangSymbols.PROCESS in target, "Missing process symbol"
    assert SynthLangSymbols.OUTPUT in target, "Missing output symbol"

def test_framework_translation_examples(config):
    """Test framework translation with specific examples."""
    lm = dspy.LM(model=config.model, api_key=config.openai_api_key)
    translator = FrameworkTranslator(lm=lm)
    
    test_cases = [
        {
            "input": "Filter data where value > 5, transform results, and calculate sum",
            "expected_output": [
                f"{SynthLangSymbols.INPUT} data{SynthLangSymbols.JOIN}value",
                f"{SynthLangSymbols.PROCESS} value>5 {SynthLangSymbols.TRANSFORM} filter",
                f"{SynthLangSymbols.PROCESS} filter {SynthLangSymbols.TRANSFORM} transform",
                f"{SynthLangSymbols.OUTPUT} transform + sum"
            ]
        },
        {
            "input": "Process stream of events, aggregate by type, output trends",
            "expected_output": [
                f"{SynthLangSymbols.INPUT} events{SynthLangSymbols.JOIN}stream",
                f"{SynthLangSymbols.PROCESS} type {SynthLangSymbols.TRANSFORM} aggregate",
                f"{SynthLangSymbols.OUTPUT} trends^2"
            ]
        },
        {
            "input": "Analyze sentiment from multiple sources and generate report",
            "expected_output": [
                f"{SynthLangSymbols.INPUT} sources{SynthLangSymbols.JOIN}sentiment",
                f"{SynthLangSymbols.PROCESS} sentiment>0 {SynthLangSymbols.TRANSFORM} pos",
                f"{SynthLangSymbols.PROCESS} sentiment<0 {SynthLangSymbols.TRANSFORM} neg",
                f"{SynthLangSymbols.OUTPUT} report + trends"
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
            assert len(actual) <= FormatRules.MAX_LINE_LENGTH, \
                f"Line exceeds {FormatRules.MAX_LINE_LENGTH} characters: {actual}"
            
            # Verify proper symbol usage
            if SynthLangSymbols.INPUT in expected:
                assert SynthLangSymbols.JOIN in actual, "Input line missing item separator"

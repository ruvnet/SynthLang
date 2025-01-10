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
    def example_function():
        print("Hello World")
    """
    
    # Mock translation to test format
    translation = translator.translate(test_input)
    assert isinstance(translation, dict)
    assert "source" in translation
    assert "target" in translation
    assert "explanation" in translation

def test_system_prompt_generation_format(lm):
    """Test system prompt generation output format."""
    generator = SystemPromptGenerator(lm)
    
    test_input = "Create a chatbot that helps users learn Python"
    
    # Mock generation to test format
    prompt = generator.generate(test_input)
    assert isinstance(prompt, dict)
    assert "prompt" in prompt
    assert "rationale" in prompt
    assert "metadata" in prompt

@pytest.mark.integration
def test_framework_translation_integration(lm):
    """Integration test for framework translation."""
    translator = FrameworkTranslator(lm)
    
    test_input = """
    // React component
    function Counter() {
        const [count, setCount] = useState(0);
        return (
            <div>
                <p>Count: {count}</p>
                <button onClick={() => setCount(count + 1)}>
                    Increment
                </button>
            </div>
        );
    }
    """
    
    translation = translator.translate(test_input)
    assert translation["source"].strip() == test_input.strip()
    assert "Vue" in translation["target"] or "Angular" in translation["target"]
    assert len(translation["explanation"]) > 0

@pytest.mark.integration
def test_system_prompt_generation_integration(lm):
    """Integration test for system prompt generation."""
    generator = SystemPromptGenerator(lm)
    
    test_input = "Create an AI assistant that helps with code review"
    
    prompt = generator.generate(test_input)
    assert len(prompt["prompt"]) > 0
    assert len(prompt["rationale"]) > 0
    assert isinstance(prompt["metadata"], dict)

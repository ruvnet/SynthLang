"""SynthLang CLI package."""
from synthlang.config import Config, ConfigManager
from synthlang.core import (
    SynthLangModule,
    FrameworkTranslator,
    SystemPromptGenerator
)

__version__ = "0.1.0"

__all__ = [
    "Config",
    "ConfigManager",
    "SynthLangModule",
    "FrameworkTranslator",
    "SystemPromptGenerator",
    "__version__"
]

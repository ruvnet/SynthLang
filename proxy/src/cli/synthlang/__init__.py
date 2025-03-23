"""SynthLang CLI package."""
from synthlang.config import Config, ConfigManager
from synthlang.core import (
    SynthLangModule,
    FrameworkTranslator,
    SystemPromptGenerator
)

__version__ = "0.2.0"

# Import proxy module to make it available
try:
    from synthlang import proxy
except ImportError:
    # Proxy module might not be available in some environments
    proxy = None

__all__ = [
    "Config",
    "ConfigManager",
    "SynthLangModule",
    "FrameworkTranslator",
    "SystemPromptGenerator",
    "proxy",
    "__version__"
]

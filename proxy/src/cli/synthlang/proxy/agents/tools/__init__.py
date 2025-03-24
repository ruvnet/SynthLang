"""Built-in tools for SynthLang agents."""

# Import built-in tools to register them
from synthlang.proxy.agents.tools import (
    file_tools,
    web_tools,
    math_tools
)

__all__ = [
    "file_tools",
    "web_tools",
    "math_tools"
]
"""
Calculator tool for the SynthLang Proxy.

This module provides a tool for performing mathematical calculations.
"""
import logging
import re
import sys
import os
import traceback
from typing import Dict, Any, Optional
import math

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path in calculator.py")

# Print current Python path for debugging
print(f"Python path in calculator.py: {sys.path}")

# Try to import from src.app first
try:
    print("Attempting to import registry from src.app.agents.registry")
    from src.app.agents.registry import register_tool
    print("Successfully imported registry from src.app.agents.registry")
except ImportError as e:
    print(f"Error importing from src.app.agents.registry: {e}")
    print(f"Traceback: {traceback.format_exc()}")
    # Try to import from app
    try:
        print("Attempting to import registry from app.agents.registry")
        from app.agents.registry import register_tool
        print("Successfully imported registry from app.agents.registry")
    except ImportError as e2:
        print(f"Error importing from app.agents.registry: {e2}")
        print(f"Traceback: {traceback.format_exc()}")
        # Re-raise the original exception
        raise e

# Logger for this module
logger = logging.getLogger(__name__)

async def calculate(expression: str, user_message: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Calculate the result of a mathematical expression.
    
    Args:
        expression: The mathematical expression to evaluate
        user_message: The original user message (optional)
        user_id: The ID of the user making the request (optional)
        
    Returns:
        A dictionary containing the calculation result
    """
    logger.info(f"Calculating expression: {expression}")
    print(f"Calculating expression: {expression}")
    
    # Clean the expression
    expression = expression.strip()
    
    # Replace common words with symbols
    expression = expression.replace('plus', '+')
    expression = expression.replace('minus', '-')
    expression = expression.replace('times', '*')
    expression = expression.replace('divided by', '/')
    expression = expression.replace('divided', '/')
    expression = expression.replace('over', '/')
    expression = expression.replace('multiplied by', '*')
    expression = expression.replace('x', '*')
    expression = expression.replace('^', '**')
    
    # Remove any characters that aren't allowed in mathematical expressions
    expression = re.sub(r'[^0-9+\-*/().%\s]', '', expression)
    
    try:
        # Add math functions to the evaluation context
        safe_dict = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'pow': pow,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e
        }
        
        # Evaluate the expression in a safe context
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        
        # Format the result
        if isinstance(result, int) or (isinstance(result, float) and result.is_integer()):
            formatted_result = str(int(result))
        else:
            formatted_result = str(round(result, 6))
        
        # Create the response
        response = f"""Calculation result:

Expression: {expression}
Result: {formatted_result}

This calculation was performed using the calculator tool."""
        
        print(f"Calculation result: {formatted_result}")
        
        return {
            "content": response,
            "tool": "calculator",
            "expression": expression,
            "result": formatted_result
        }
    
    except Exception as e:
        error_message = f"""I couldn't calculate the expression "{expression}".

Error: {str(e)}

Please check that your expression is valid and try again. Here are some examples of valid expressions:
- 2 + 2
- 10 * 5
- (3 + 4) * 2
- 10 / 2
- 2 ** 3 (for exponentiation)"""
        
        print(f"Calculation error: {str(e)}")
        
        return {
            "content": error_message,
            "tool": "calculator",
            "expression": expression,
            "error": str(e)
        }

# Register the tool
try:
    print("Registering calculator tool")
    register_tool("calculator", calculate)
    print("Calculator tool registered successfully")
except Exception as e:
    print(f"Error registering calculator tool: {e}")
    print(f"Traceback: {traceback.format_exc()}")
"""
Calculator tool for agent tools.

This module provides a calculator tool for agent tools.
"""
import logging
import re
from typing import Dict, Any

from src.app.agents.tools.registry import register_tool

# Configure logging
logger = logging.getLogger(__name__)


async def calculator(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate a mathematical expression.
    
    Args:
        parameters: Tool parameters
            - expression: Mathematical expression to calculate
            
    Returns:
        Dictionary containing the calculation result
    """
    # Get expression from parameters
    expression = parameters.get("expression", "")
    
    if not expression:
        raise ValueError("Expression is required")
    
    # Sanitize expression to prevent code execution
    sanitized = sanitize_expression(expression)
    
    # Calculate expression
    try:
        # Track calculation steps
        steps = []
        
        # Handle parentheses first
        while "(" in sanitized:
            # Find innermost parentheses
            match = re.search(r"\([^()]*\)", sanitized)
            if not match:
                break
                
            # Calculate expression inside parentheses
            inner_expr = match.group(0)[1:-1]  # Remove parentheses
            inner_result = calculate_simple_expression(inner_expr)
            steps.append(f"Calculate {match.group(0)} = {inner_result}")
            
            # Replace parentheses with result
            sanitized = sanitized[:match.start()] + str(inner_result) + sanitized[match.end():]
        
        # Calculate final expression
        result = calculate_simple_expression(sanitized)
        steps.append(f"Calculate {sanitized} = {result}")
        
        return {
            "value": result,
            "expression": expression,
            "steps": steps
        }
    except Exception as e:
        logger.error(f"Calculator error: {e}")
        raise ValueError(f"Failed to calculate expression: {str(e)}")


def sanitize_expression(expression: str) -> str:
    """
    Sanitize a mathematical expression to prevent code execution.
    
    Args:
        expression: Mathematical expression
        
    Returns:
        Sanitized expression
    """
    # Remove all whitespace
    sanitized = re.sub(r"\s+", "", expression)
    
    # Only allow numbers, operators, and parentheses
    if not re.match(r"^[0-9+\-*/().]+$", sanitized):
        raise ValueError("Expression contains invalid characters")
    
    return sanitized


def calculate_simple_expression(expression: str) -> float:
    """
    Calculate a simple mathematical expression without parentheses.
    
    Args:
        expression: Mathematical expression
        
    Returns:
        Calculation result
    """
    # Handle multiplication and division first
    while "*" in expression or "/" in expression:
        # Find multiplication or division
        match = re.search(r"(\d+\.?\d*)[*/](\d+\.?\d*)", expression)
        if not match:
            break
            
        # Calculate result
        a = float(match.group(1))
        op = match.group(0)[len(match.group(1))]
        b = float(match.group(2))
        
        if op == "*":
            result = a * b
        else:
            if b == 0:
                raise ValueError("Division by zero")
            result = a / b
        
        # Replace expression with result
        expression = expression[:match.start()] + str(result) + expression[match.end():]
    
    # Handle addition and subtraction
    while "+" in expression or "-" in expression:
        # Find addition or subtraction
        match = re.search(r"(\d+\.?\d*)[+\-](\d+\.?\d*)", expression)
        if not match:
            break
            
        # Calculate result
        a = float(match.group(1))
        op = match.group(0)[len(match.group(1))]
        b = float(match.group(2))
        
        if op == "+":
            result = a + b
        else:
            result = a - b
        
        # Replace expression with result
        expression = expression[:match.start()] + str(result) + expression[match.end():]
    
    # Return final result
    return float(expression)


# Register tool
register_tool(
    name="calculator",
    description="Calculate a mathematical expression",
    function=calculator,
    parameters={
        "expression": {
            "type": "string",
            "description": "Mathematical expression to calculate"
        }
    },
    required_role="basic"
)
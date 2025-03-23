"""Math tools for SynthLang agents."""
import math
import random
import statistics
from typing import List, Dict, Any, Union, Optional

from synthlang.proxy.agents.registry import register_tool
from synthlang.utils.logger import get_logger

logger = get_logger(__name__)


@register_tool(description="Evaluate a mathematical expression")
def evaluate_expression(expression: str) -> float:
    """Evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        Result of the evaluation
        
    Raises:
        ValueError: If expression is invalid
    """
    # Use safer eval with restricted globals
    allowed_names = {
        k: v for k, v in math.__dict__.items() 
        if not k.startswith('__')
    }
    allowed_names.update({
        'abs': abs,
        'round': round,
        'min': min,
        'max': max
    })
    
    try:
        return float(eval(expression, {"__builtins__": {}}, allowed_names))
    except Exception as e:
        logger.error(f"Error evaluating expression '{expression}': {str(e)}")
        raise ValueError(f"Invalid expression: {str(e)}")


@register_tool(description="Calculate basic statistics for a list of numbers")
def calculate_statistics(
    numbers: List[float]
) -> Dict[str, float]:
    """Calculate basic statistics for a list of numbers.
    
    Args:
        numbers: List of numbers
        
    Returns:
        Dictionary with statistics
        
    Raises:
        ValueError: If input is invalid
    """
    if not numbers:
        raise ValueError("Input list is empty")
    
    try:
        # Convert all values to float
        float_numbers = [float(n) for n in numbers]
        
        result = {
            "count": len(float_numbers),
            "min": min(float_numbers),
            "max": max(float_numbers),
            "sum": sum(float_numbers),
            "mean": statistics.mean(float_numbers),
            "median": statistics.median(float_numbers),
            "range": max(float_numbers) - min(float_numbers)
        }
        
        # Add standard deviation and variance if there's more than one number
        if len(float_numbers) > 1:
            result["std_dev"] = statistics.stdev(float_numbers)
            result["variance"] = statistics.variance(float_numbers)
        
        return result
    except Exception as e:
        logger.error(f"Error calculating statistics: {str(e)}")
        raise ValueError(f"Error calculating statistics: {str(e)}")


@register_tool(description="Generate random numbers")
def generate_random_numbers(
    count: int = 1,
    min_value: float = 0.0,
    max_value: float = 1.0,
    integer_only: bool = False
) -> List[Union[int, float]]:
    """Generate random numbers.
    
    Args:
        count: Number of random numbers to generate
        min_value: Minimum value (inclusive)
        max_value: Maximum value (inclusive for integers, exclusive for floats)
        integer_only: Whether to generate integers only
        
    Returns:
        List of random numbers
        
    Raises:
        ValueError: If parameters are invalid
    """
    if count <= 0:
        raise ValueError("Count must be positive")
    
    if min_value >= max_value:
        raise ValueError("min_value must be less than max_value")
    
    try:
        if integer_only:
            return [random.randint(int(min_value), int(max_value)) for _ in range(count)]
        else:
            return [random.uniform(min_value, max_value) for _ in range(count)]
    except Exception as e:
        logger.error(f"Error generating random numbers: {str(e)}")
        raise ValueError(f"Error generating random numbers: {str(e)}")


@register_tool(description="Convert between units")
def convert_units(
    value: float,
    from_unit: str,
    to_unit: str
) -> float:
    """Convert between units.
    
    Supported unit types:
    - Length: mm, cm, m, km, in, ft, yd, mi
    - Weight/Mass: mg, g, kg, oz, lb, ton
    - Temperature: C, F, K
    - Time: s, min, h, day
    - Area: mm2, cm2, m2, km2, in2, ft2, yd2, mi2, ha, acre
    - Volume: ml, l, m3, gal, qt, pt, cup, oz_fl
    
    Args:
        value: Value to convert
        from_unit: Source unit
        to_unit: Target unit
        
    Returns:
        Converted value
        
    Raises:
        ValueError: If conversion is not supported
    """
    # Define conversion factors to SI units
    length_units = {
        "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
        "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344
    }
    
    weight_units = {
        "mg": 0.000001, "g": 0.001, "kg": 1,
        "oz": 0.028349523125, "lb": 0.45359237, "ton": 907.18474
    }
    
    area_units = {
        "mm2": 0.000001, "cm2": 0.0001, "m2": 1, "km2": 1000000,
        "in2": 0.00064516, "ft2": 0.09290304, "yd2": 0.83612736, "mi2": 2589988.110336,
        "ha": 10000, "acre": 4046.8564224
    }
    
    volume_units = {
        "ml": 0.000001, "l": 0.001, "m3": 1,
        "gal": 0.003785411784, "qt": 0.000946352946, "pt": 0.000473176473,
        "cup": 0.000236588236, "oz_fl": 0.0000295735295625
    }
    
    time_units = {
        "s": 1, "min": 60, "h": 3600, "day": 86400
    }
    
    # Group units by type
    unit_groups = {
        "length": length_units,
        "weight": weight_units,
        "area": area_units,
        "volume": volume_units,
        "time": time_units
    }
    
    # Special case for temperature
    if from_unit in ["C", "F", "K"] and to_unit in ["C", "F", "K"]:
        # Convert to Kelvin first
        if from_unit == "C":
            kelvin = value + 273.15
        elif from_unit == "F":
            kelvin = (value - 32) * 5/9 + 273.15
        else:  # K
            kelvin = value
        
        # Convert from Kelvin to target
        if to_unit == "C":
            return kelvin - 273.15
        elif to_unit == "F":
            return (kelvin - 273.15) * 9/5 + 32
        else:  # K
            return kelvin
    
    # Find which group the units belong to
    group_name = None
    for name, units in unit_groups.items():
        if from_unit in units and to_unit in units:
            group_name = name
            break
    
    if group_name is None:
        raise ValueError(f"Cannot convert from {from_unit} to {to_unit}")
    
    # Get the conversion factors
    units = unit_groups[group_name]
    
    # Convert to SI then to target unit
    si_value = value * units[from_unit]
    return si_value / units[to_unit]


@register_tool(description="Solve a linear equation")
def solve_linear_equation(equation: str, variable: str = "x") -> float:
    """Solve a simple linear equation.
    
    Args:
        equation: Linear equation to solve (e.g., "2*x + 3 = 7")
        variable: Variable to solve for
        
    Returns:
        Solution to the equation
        
    Raises:
        ValueError: If equation is invalid or not linear
    """
    try:
        import sympy
        
        # Parse the equation
        eq = sympy.sympify("Eq(" + equation.replace("=", ",") + ")")
        
        # Solve for the variable
        var = sympy.Symbol(variable)
        solution = sympy.solve(eq, var)[0]
        
        # Convert to float if possible
        try:
            return float(solution)
        except TypeError:
            return solution
    except Exception as e:
        logger.error(f"Error solving equation '{equation}': {str(e)}")
        raise ValueError(f"Error solving equation: {str(e)}")
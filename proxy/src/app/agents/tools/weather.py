"""
Weather tool for the SynthLang Proxy.

This module provides a tool for getting weather information.
"""
import logging
import random
from typing import Dict, Any, Optional

from app.agents.registry import register_tool

# Logger for this module
logger = logging.getLogger(__name__)

async def get_weather(location: str, user_message: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Get weather information for a location.
    
    Args:
        location: The location to get weather for
        user_message: The original user message (optional)
        user_id: The ID of the user making the request (optional)
        
    Returns:
        A dictionary containing the weather information
    """
    logger.info(f"Getting weather for location: {location}")
    
    # In a real implementation, this would call a weather API
    # For this example, we'll just return some random weather data
    
    # List of possible weather conditions
    conditions = ["sunny", "partly cloudy", "cloudy", "rainy", "thunderstorms", "snowy", "windy", "foggy"]
    
    # Generate random temperature (°F)
    temp_f = random.randint(30, 95)
    temp_c = round((temp_f - 32) * 5/9, 1)
    
    # Generate random humidity
    humidity = random.randint(30, 90)
    
    # Generate random wind speed
    wind_speed = random.randint(0, 30)
    
    # Select a random condition
    condition = random.choice(conditions)
    
    # Create a weather report
    weather_report = f"""Current weather for {location}:
- Condition: {condition}
- Temperature: {temp_f}°F ({temp_c}°C)
- Humidity: {humidity}%
- Wind Speed: {wind_speed} mph

This is simulated weather data for demonstration purposes."""
    
    return {
        "content": weather_report,
        "tool": "weather",
        "location": location
    }

# Register the tool
register_tool("weather", get_weather)
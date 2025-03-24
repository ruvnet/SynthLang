"""
Database interaction functions.

This module provides functions for interacting with the database,
including saving interaction data with encryption.
"""
from src.app.database import SessionLocal, Interaction
from src.app import security  # Import security module for encryption


async def save_interaction(user_id: str, model: str, messages: list, response_text: str, cache_hit: bool):
    """
    Save the interaction (prompt and response) to the database with encryption.
    
    Args:
        user_id: The user identifier
        model: The LLM model used
        messages: The conversation messages
        response_text: The LLM response text
        cache_hit: Whether the response was from cache
        
    Returns:
        None
    """
    # Combine messages to prompt text
    prompt_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    
    # Encrypt data using security module
    prompt_enc = security.encrypt_text(prompt_text)  # Encrypt prompt
    response_enc = security.encrypt_text(response_text)  # Encrypt response
    
    # Placeholder token count
    prompt_tokens = len(prompt_text.split())  # Placeholder token count
    response_tokens = len(response_text.split())  # Placeholder token count
    
    # Create and save interaction record
    async with SessionLocal() as session:  # Async session
        interaction = Interaction(  # Create Interaction object
            user_id=user_id,
            model=model,
            prompt_enc=prompt_enc,
            response_enc=response_enc,
            cache_hit=cache_hit,
            prompt_tokens=prompt_tokens,
            response_tokens=response_tokens
        )
        session.add(interaction)  # Add to session
        await session.commit()  # Commit transaction
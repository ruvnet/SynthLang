"""
Tests for database persistence functionality.

This module contains tests for the database persistence functionality.
"""
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pytest_asyncio
from unittest.mock import patch, MagicMock

from app import db
from app.database import Interaction, Base


# Use an in-memory SQLite database for tests
DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def test_db_session():
    """Create a test database session."""
    # Create engine and session
    engine = create_async_engine(DATABASE_URL_TEST)
    TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create and return a session
    async with TestingSessionLocal() as session:
        # Store original session
        original_session = db.SessionLocal
        
        # Replace with test session
        db.SessionLocal = TestingSessionLocal
        
        yield session
        
        # Restore original
        db.SessionLocal = original_session
    
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_save_interaction_success(test_db_session):
    """Test that an interaction can be successfully saved to the database with encryption."""
    # Test data
    user_id = "test_user"
    model = "test-model"
    messages = [{"role": "user", "content": "Test prompt with sensitive info: test@example.com"}]
    response_text = "Test response with phone number 123-456-7890"
    cache_hit = False
    
    # Create a mock for the security module
    mock_security = MagicMock()
    mock_security.encrypt_text.side_effect = lambda text: text.encode('utf-8')
    mock_security.decrypt_text.side_effect = lambda text: text.decode('utf-8')
    
    # Patch the security module in the db module
    with patch.object(db, 'security', mock_security):
        # Save interaction
        await db.save_interaction(user_id, model, messages, response_text, cache_hit)
        
        # Verify it was saved correctly
        result = await test_db_session.execute(
            text("SELECT user_id, model, prompt_enc, response_enc, cache_hit FROM interactions ORDER BY id DESC LIMIT 1")
        )
        row = result.fetchone()
        
        assert row is not None
        db_user_id, db_model, db_prompt_enc, db_response_enc, db_cache_hit = row
        
        assert db_user_id == user_id
        assert db_model == model
        assert db_cache_hit == cache_hit
        
        # Decrypt and verify content using our mock
        decrypted_prompt = mock_security.decrypt_text(db_prompt_enc)
        decrypted_response = mock_security.decrypt_text(db_response_enc)
        
        assert decrypted_prompt == "user: Test prompt with sensitive info: test@example.com"
        assert decrypted_response == response_text


@pytest.mark.asyncio
async def test_save_interaction_with_multiple_messages(test_db_session):
    """Test saving an interaction with multiple messages."""
    # Test data
    user_id = "test_user"
    model = "test-model"
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "How are you?"}
    ]
    response_text = "I'm doing well, thank you for asking!"
    cache_hit = True
    
    # Create a mock for the security module
    mock_security = MagicMock()
    mock_security.encrypt_text.side_effect = lambda text: text.encode('utf-8')
    mock_security.decrypt_text.side_effect = lambda text: text.decode('utf-8')
    
    # Patch the security module in the db module
    with patch.object(db, 'security', mock_security):
        # Save interaction
        await db.save_interaction(user_id, model, messages, response_text, cache_hit)
        
        # Verify it was saved correctly
        result = await test_db_session.execute(
            text("SELECT prompt_enc, response_enc, cache_hit FROM interactions ORDER BY id DESC LIMIT 1")
        )
        row = result.fetchone()
        
        assert row is not None
        db_prompt_enc, db_response_enc, db_cache_hit = row
        
        expected_prompt = (
            "system: You are a helpful assistant\n"
            "user: Hello\n"
            "assistant: Hi there!\n"
            "user: How are you?"
        )
        
        # Decrypt and verify content using our mock
        decrypted_prompt = mock_security.decrypt_text(db_prompt_enc)
        decrypted_response = mock_security.decrypt_text(db_response_enc)
        
        assert decrypted_prompt == expected_prompt
        assert decrypted_response == response_text
        assert db_cache_hit == cache_hit
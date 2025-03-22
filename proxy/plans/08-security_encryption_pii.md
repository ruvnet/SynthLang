# Phase 8: Security - Encryption and PII Masking (08-security_encryption_pii.md)

## Objective
Implement security features: encryption of stored prompts/responses and PII masking.

## Steps

1.  **Create `app/security.py` file:**
    -   Create `app/security.py` to house security-related functions.

2.  **Implement Encryption Functions in `app/security.py`:**
    -   Import `cryptography.fernet` and `os` modules.
    -   Initialize Fernet cipher:
        -   Get `ENCRYPTION_KEY` from environment variables.
        -   If not found, generate a new Fernet key (for development, in production, key should be properly managed).
        -   Create `cipher = Fernet(FERNET_KEY)`.
    -   Implement `encrypt_text(plain: str) -> bytes` function:
        -   Encrypt the input `plain` text using `cipher.encrypt()` and return the encrypted bytes.
    -   Implement `decrypt_text(token: bytes) -> str` function:
        -   Decrypt the input `token` bytes using `cipher.decrypt()` and return the decrypted text (decoded to UTF-8).

    ```python
    # app/security.py
    from cryptography.fernet import Fernet
    import os

    FERNET_KEY = os.environ.get("ENCRYPTION_KEY") # Get key from env var
    if not FERNET_KEY: # Generate key if not found (for development, not production)
        FERNET_KEY = Fernet.generate_key()
        print("Warning: ENCRYPTION_KEY not found in environment, generated a new key. Ensure to set it in production.")
    cipher = Fernet(FERNET_KEY) # Initialize Fernet cipher

    def encrypt_text(plain: str) -> bytes:
        """Encrypt text to bytes using Fernet symmetric encryption."""
        return cipher.encrypt(plain.encode('utf-8'))

    def decrypt_text(token: bytes) -> str:
        """Decrypt bytes to text using Fernet."""
        return cipher.decrypt(token).decode('utf-8')
    ```

3.  **Implement PII Masking Function in `app/security.py`:**
    -   Import `re` module.
    -   Define `PII_PATTERNS` list of tuples: `(regex_pattern, placeholder_string)` for PII patterns (e.g., email, phone numbers). Start with basic regex patterns.
    -   Implement `mask_pii(text: str) -> str` function:
        -   Iterate through `PII_PATTERNS`.
        -   For each pattern, use `re.sub()` to replace matches in the input `text` with the corresponding `placeholder_string`.
        -   Return the masked text.

    ```python
    # app/security.py (add PII masking to existing file)
    from cryptography.fernet import Fernet
    import os
    import re # Import re for regex

    FERNET_KEY = os.environ.get("ENCRYPTION_KEY")
    if not FERNET_KEY:
        FERNET_KEY = Fernet.generate_key()
        print("Warning: ENCRYPTION_KEY not found in environment, generated a new key. Ensure to set it in production.")
    cipher = Fernet(FERNET_KEY)

    def encrypt_text(plain: str) -> bytes: # Existing function, keep it
        return cipher.encrypt(plain.encode('utf-8'))

    def decrypt_text(token: bytes) -> str: # Existing function, keep it
        return cipher.decrypt(token).decode('utf-8')

    PII_PATTERNS = [ # Define PII patterns (basic examples)
        (re.compile(r'\S+@\S+\.\S+'), '<EMAIL_ADDRESS>'), # Email regex
        (re.compile(r'\b\d{10}\b'), '<PHONE_NUMBER>'), # 10-digit phone number
        (re.compile(r'\b\d{3}-\d{3}-\d{4}\b'), '<PHONE_NUMBER>') # Phone number format 123-456-7890
    ]

    def mask_pii(text: str) -> str:
        """Mask PII in text using regex patterns."""
        masked = text
        for pattern, placeholder in PII_PATTERNS:
            masked = pattern.sub(placeholder, masked) # Replace PII with placeholders
        return masked
    ```

4.  **Integrate Security Features in `app/db.py`:**
    -   Import `security` from `app.security`.
    -   In `save_interaction` function:
        -   Use `security.encrypt_text(prompt_text)` and `security.encrypt_text(response_text)` to encrypt prompt and response text before storing them as `prompt_enc` and `response_enc` in the database.
        -   (Optional, for later phase) Implement PII masking: before encryption, call `security.mask_pii(prompt_text)` and `security.mask_pii(response_text)` if PII masking is enabled via a config flag. For now, focus on encryption.

    ```python
    # app/db.py
    from app.database import SessionLocal, Interaction
    from app import security # Import security

    async def save_interaction(user_id: str, model: str, messages: list, response_text: str, cache_hit: bool):
        """Save the interaction (prompt and response) to the database with encryption."""
        prompt_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        # Encryption using security module
        prompt_enc = security.encrypt_text(prompt_text) # Encrypt prompt
        response_enc = security.encrypt_text(response_text) # Encrypt response
        prompt_tokens = len(prompt_text.split()) # Placeholder token count
        response_tokens = len(response_text.split()) # Placeholder token count

        async with SessionLocal() as session:
            interaction = Interaction(
                user_id=user_id,
                model=model,
                prompt_enc=prompt_enc,
                response_enc=response_enc,
                cache_hit=cache_hit,
                prompt_tokens=prompt_tokens,
                response_tokens=response_tokens
            )
            session.add(interaction)
            await session.commit()
    ```

5.  **Update `tests/test_db.py` to test Encryption:**
    -   In `test_save_interaction_success` in `tests/test_db.py`:
        -   After saving and retrieving the interaction, decrypt `db_prompt_enc` and `db_response_enc` using `security.decrypt_text()`.
        -   Assert that the decrypted prompt and response text match the original `prompt_text` and `response_text`.

    ```python
    # tests/test_db.py (update existing test)
    import asyncio
    from app import db, database, security # Import security
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    import pytest

    # ... (rest of test_db.py setup remains the same)

    @pytest.mark.asyncio
    async def test_save_interaction_success(): # Update existing test to check encryption
        user_id = "test_user"
        model = "test-model"
        messages = [{"role": "user", "content": "Test prompt with sensitive info: test@example.com"}] # Include potential PII
        response_text = "Test response with phone number 123-456-7890" # Include potential PII
        cache_hit = False
        await db.save_interaction(user_id, model, messages, response_text, cache_hit) # Save interaction

        async def get_last_interaction(): # Helper, keep it
            async with TestingSessionLocal() as session:
                result = await session.execute("SELECT user_id, model, prompt_enc, response_enc, cache_hit FROM interactions ORDER BY id DESC LIMIT 1")
                row = result.fetchone()
                return row

        row = await get_last_interaction()
        assert row is not None
        db_user_id, db_model, db_prompt_enc, db_response_enc, db_cache_hit = row
        assert db_user_id == user_id
        assert db_model == model
        assert db_cache_hit == cache_hit
        
        # Decrypt and verify content
        decrypted_prompt_text = security.decrypt_text(db_prompt_enc) # Decrypt prompt
        decrypted_response_text = security.decrypt_text(db_response_enc) # Decrypt response
        assert decrypted_prompt_text == "\nuser: Test prompt with sensitive info: test@example.com" # Check decrypted prompt
        assert decrypted_response_text == response_text # Check decrypted response (original response_text is without PII masking for now)
```

6.  **Create test file `tests/test_security.py`:**
    -   Create `tests/test_security.py` for security function tests.

7.  **Write tests for Security Functions in `tests/test_security.py`:**
    -   Test `encrypt_text` and `decrypt_text` functions:
        -   **Encryption and Decryption Round-Trip:** Test that encrypting and then decrypting a text restores the original text.
    -   Test `mask_pii` function:
        -   **PII Masking:** Test that `mask_pii` function correctly masks email addresses and phone numbers in a sample text.
        -   **No False Positives:** Test that `mask_pii` does not modify text that does not contain PII.

    ```python
    # tests/test_security.py
    from app import security

    def test_encrypt_decrypt_round_trip():
        original_text = "This is a secret message to be encrypted."
        encrypted_text = security.encrypt_text(original_text)
        decrypted_text = security.decrypt_text(encrypted_text)
        assert decrypted_text == original_text # Round-trip test

    def test_mask_pii_basic():
        text_with_pii = "Contact us at test@example.com or call 555-123-4567."
        masked_text = security.mask_pii(text_with_pii)
        assert "<EMAIL_ADDRESS>" in masked_text # Check for email placeholder
        assert "<PHONE_NUMBER>" in masked_text # Check for phone placeholder
        assert "test@example.com" not in masked_text # Original email should be masked
        assert "555-123-4567" not in masked_text # Original phone should be masked

    def test_mask_pii_no_false_positives():
        clean_text = "This text has no PII."
        masked_text = security.mask_pii(clean_text)
        assert masked_text == clean_text # Should not modify clean text
    ```

8.  **Run tests using Pytest:**
    -   Navigate to the `synthlang_router/` directory in the terminal.
    -   Run `pytest tests/test_security.py tests/test_db.py tests/test_api.py` to execute all tests.
    -   Ensure all tests pass.

## Test-Driven Development Checklist

-   [x] Step 1: Create `app/security.py` file.
-   [x] Step 2: Implement Encryption Functions in `app/security.py`.
-   [x] Step 3: Implement PII Masking Function in `app/security.py`.
-   [x] Step 4: Integrate Security Features in `app/db.py` (Encryption).
-   [x] Step 5: Update `tests/test_db.py` to test Encryption.
-   [x] Step 6: Create test file `tests/test_security.py`.
-   [x] Step 7: Write tests for Security Functions in `tests/test_security.py`.
-   [ ] Step 8: Run tests using Pytest and ensure all pass.

**Next Phase:** Implement OpenAI Agents SDK and Tool Registry (09-agents_sdk_tool_registry.md)

---
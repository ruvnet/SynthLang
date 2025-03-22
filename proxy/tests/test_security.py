"""
Tests for security functionality.

This module contains tests for the encryption and PII masking functionality.
"""
import pytest
from app import security


def test_encrypt_decrypt_round_trip():
    """Test that encrypting and then decrypting a text restores the original text."""
    original_text = "This is a secret message to be encrypted."
    encrypted_text = security.encrypt_text(original_text)
    decrypted_text = security.decrypt_text(encrypted_text)
    
    # Verify encrypted text is different from original
    assert encrypted_text != original_text.encode('utf-8')
    # Verify round-trip encryption/decryption works
    assert decrypted_text == original_text


def test_mask_pii_basic():
    """Test that PII masking correctly masks email addresses and phone numbers."""
    text_with_pii = "Contact us at test@example.com or call 555-123-4567."
    masked_text = security.mask_pii(text_with_pii)
    
    # Check for placeholders
    assert "<EMAIL_ADDRESS>" in masked_text
    assert "<PHONE_NUMBER>" in masked_text
    
    # Original PII should be masked
    assert "test@example.com" not in masked_text
    assert "555-123-4567" not in masked_text


def test_mask_pii_no_false_positives():
    """Test that PII masking does not modify text without PII."""
    clean_text = "This text has no PII."
    masked_text = security.mask_pii(clean_text)
    
    # Should not modify clean text
    assert masked_text == clean_text


def test_mask_pii_multiple_patterns():
    """Test that PII masking handles multiple PII patterns in the same text."""
    text_with_multiple_pii = (
        "Contact john.doe@example.com or jane.smith@company.org. "
        "Call us at 1234567890 or 555-123-4567."
    )
    masked_text = security.mask_pii(text_with_multiple_pii)
    
    # Count occurrences of placeholders
    email_count = masked_text.count("<EMAIL_ADDRESS>")
    phone_count = masked_text.count("<PHONE_NUMBER>")
    
    # Should have masked 2 emails and 2 phone numbers
    assert email_count == 2
    assert phone_count == 2
    
    # Original PII should be masked
    assert "john.doe@example.com" not in masked_text
    assert "jane.smith@company.org" not in masked_text
    assert "1234567890" not in masked_text
    assert "555-123-4567" not in masked_text
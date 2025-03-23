"""
Security-related functions for encryption and PII masking.

This module provides functions for encrypting and decrypting text data,
as well as masking personally identifiable information (PII) in text.
"""
from cryptography.fernet import Fernet
import base64
import os
import re
import logging
from src.app.config import ENCRYPTION_KEY, MASK_PII_BEFORE_LLM, MASK_PII_IN_LOGS

# Configure logging
logger = logging.getLogger(__name__)

# Get encryption key from configuration or generate a new one
def get_fernet_key():
    """
    Get a valid Fernet key from the environment or generate a new one.
    
    Returns:
        A valid Fernet key
    """
    key = ENCRYPTION_KEY
    
    if not key:
        # Generate key if not found (for development, not production)
        logger.warning("ENCRYPTION_KEY environment variable not set. Encryption/decryption will likely fail.")
        key = Fernet.generate_key().decode('utf-8')
        logger.warning("ENCRYPTION_KEY not found in configuration, generated a new key. Ensure to set it in production.")
        return key
    
    # Ensure the key is valid for Fernet (32 url-safe base64-encoded bytes)
    try:
        # If the key is already a valid Fernet key, this will work
        Fernet(key.encode('utf-8') if isinstance(key, str) else key)
        return key
    except Exception:
        # If not, try to convert it to a valid Fernet key
        try:
            # If it's a hex string, convert to bytes and then to base64
            if all(c in '0123456789abcdefABCDEF' for c in key):
                # Convert hex to bytes
                key_bytes = bytes.fromhex(key)
                # Ensure it's 32 bytes (pad or truncate)
                key_bytes = key_bytes.ljust(32, b'\0')[:32]
                # Convert to url-safe base64
                key = base64.urlsafe_b64encode(key_bytes)
                return key
            else:
                # Try to use as-is, but ensure it's 32 bytes
                key_bytes = key.encode('utf-8') if isinstance(key, str) else key
                key_bytes = key_bytes.ljust(32, b'\0')[:32]
                key = base64.urlsafe_b64encode(key_bytes)
                return key
        except Exception as e:
            # If all else fails, generate a new key
            logger.error(f"Failed to create a valid Fernet key: {e}")
            key = Fernet.generate_key()
            logger.warning("Generated a new Fernet key. This key will not persist across restarts.")
            return key

# Initialize Fernet cipher with a valid key
FERNET_KEY = get_fernet_key()
cipher = Fernet(FERNET_KEY if isinstance(FERNET_KEY, bytes) else FERNET_KEY.encode('utf-8'))


def encrypt_text(plain: str) -> bytes:
    """
    Encrypt text to bytes using Fernet symmetric encryption.
    
    Args:
        plain: The plain text to encrypt
        
    Returns:
        Encrypted bytes
    """
    return cipher.encrypt(plain.encode('utf-8'))


def decrypt_text(token: bytes) -> str:
    """
    Decrypt bytes to text using Fernet.
    
    Args:
        token: The encrypted bytes to decrypt
        
    Returns:
        Decrypted text
    """
    return cipher.decrypt(token).decode('utf-8')


# Enhanced PII patterns with more comprehensive coverage
PII_PATTERNS = [
    # Email addresses
    (re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'), '<EMAIL_ADDRESS>'),
    
    # Phone numbers (various formats)
    (re.compile(r'\b\d{10}\b'), '<PHONE_NUMBER>'),  # 10-digit phone number
    (re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'), '<PHONE_NUMBER>'),  # 123-456-7890, 123.456.7890, 123 456 7890
    (re.compile(r'\b\(\d{3}\)\s*\d{3}[-.\s]?\d{4}\b'), '<PHONE_NUMBER>'),  # (123) 456-7890
    (re.compile(r'\b\+\d{1,3}\s*\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'), '<PHONE_NUMBER>'),  # +1 123-456-7890
    
    # Social Security Numbers
    (re.compile(r'\b\d{3}[-]?\d{2}[-]?\d{4}\b'), '<SSN>'),  # 123-45-6789 or 123456789
    
    # Credit Card Numbers (basic patterns)
    (re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b'), '<CREDIT_CARD>'),  # 1234-5678-9012-3456
    (re.compile(r'\b\d{16}\b'), '<CREDIT_CARD>'),  # 1234567890123456
    
    # IP Addresses
    (re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'), '<IP_ADDRESS>'),  # IPv4
    
    # Dates (common formats)
    (re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'), '<DATE>'),  # MM/DD/YYYY, DD/MM/YYYY
    
    # Street Addresses (basic pattern)
    (re.compile(r'\b\d+\s+[A-Za-z0-9\s,]+(?:Avenue|Ave|Street|St|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Court|Ct|Way|Place|Pl)\b', 
                re.IGNORECASE), '<STREET_ADDRESS>'),
    
    # Passport Numbers (basic US format)
    (re.compile(r'\b[A-Z]{1,2}\d{6,9}\b'), '<PASSPORT_NUMBER>')
]


def mask_pii(text: str) -> str:
    """
    Mask PII in text using regex patterns.
    
    Args:
        text: The text to mask PII in
        
    Returns:
        Text with PII masked
    """
    if not text:
        return text
        
    masked = text
    for pattern, placeholder in PII_PATTERNS:
        masked = pattern.sub(placeholder, masked)  # Replace PII with placeholders
    
    # Log if PII was detected and masked
    if masked != text:
        logger.info("PII detected and masked in text")
        
    return masked


def should_mask_pii_before_llm() -> bool:
    """
    Check if PII should be masked before sending to LLM.
    
    Returns:
        True if PII should be masked before sending to LLM, False otherwise
    """
    return MASK_PII_BEFORE_LLM


def should_mask_pii_in_logs() -> bool:
    """
    Check if PII should be masked in logs and database.
    
    Returns:
        True if PII should be masked in logs and database, False otherwise
    """
    return MASK_PII_IN_LOGS
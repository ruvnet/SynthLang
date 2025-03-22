"""
Security-related functions for encryption and PII masking.

This module provides functions for encrypting and decrypting text data,
as well as masking personally identifiable information (PII) in text.
"""
from cryptography.fernet import Fernet
import re
import logging
from app.config import ENCRYPTION_KEY, MASK_PII_BEFORE_LLM, MASK_PII_IN_LOGS

# Configure logging
logger = logging.getLogger(__name__)

# Get encryption key from configuration
FERNET_KEY = ENCRYPTION_KEY
if not FERNET_KEY:
    # Generate key if not found (for development, not production)
    FERNET_KEY = Fernet.generate_key()
    logger.warning("ENCRYPTION_KEY not found in configuration, generated a new key. Ensure to set it in production.")
cipher = Fernet(FERNET_KEY)  # Initialize Fernet cipher


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


# Define PII patterns (basic examples)
PII_PATTERNS = [
    (re.compile(r'\S+@\S+\.\S+'), '<EMAIL_ADDRESS>'),  # Email regex
    (re.compile(r'\b\d{10}\b'), '<PHONE_NUMBER>'),  # 10-digit phone number
    (re.compile(r'\b\d{3}-\d{3}-\d{4}\b'), '<PHONE_NUMBER>')  # Phone number format 123-456-7890
]


def mask_pii(text: str) -> str:
    """
    Mask PII in text using regex patterns.
    
    Args:
        text: The text to mask PII in
        
    Returns:
        Text with PII masked
    """
    masked = text
    for pattern, placeholder in PII_PATTERNS:
        masked = pattern.sub(placeholder, masked)  # Replace PII with placeholders
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
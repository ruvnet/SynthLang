"""
Security-related functions for encryption and PII masking.

This module provides functions for encrypting and decrypting text data,
as well as masking personally identifiable information (PII) in text.
"""
from cryptography.fernet import Fernet
import os
import re

# Get encryption key from environment variables
FERNET_KEY = os.environ.get("ENCRYPTION_KEY")
if not FERNET_KEY:
    # Generate key if not found (for development, not production)
    FERNET_KEY = Fernet.generate_key()
    print("Warning: ENCRYPTION_KEY not found in environment, generated a new key. Ensure to set it in production.")
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
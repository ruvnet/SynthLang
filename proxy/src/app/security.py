"""
Security-related functions for encryption and PII masking.

This module provides functions for encrypting and decrypting text data,
as well as masking personally identifiable information (PII) in text.
"""
from cryptography.fernet import Fernet
import re
import logging
from src.app.config import ENCRYPTION_KEY, MASK_PII_BEFORE_LLM, MASK_PII_IN_LOGS

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
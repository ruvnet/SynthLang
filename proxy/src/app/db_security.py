"""
Database security module for SQLite.

This module provides functions for securing SQLite databases, including
file permissions, encryption, and access control.
"""
import os
import stat
import logging
import sqlite3
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
import threading
from contextlib import contextmanager

from src.app.security import encrypt_text, decrypt_text
from src.app.config import SQLITE_PATH

# Configure logging
logger = logging.getLogger(__name__)

# Extract the SQLite file path from the connection string
def get_sqlite_path() -> str:
    """
    Extract the SQLite file path from the connection string.
    
    Returns:
        The path to the SQLite database file
    """
    if not SQLITE_PATH or "sqlite" not in SQLITE_PATH:
        logger.warning("SQLITE_PATH not set or not a SQLite connection string")
        return "synthlang_proxy.db"
    
    # Remove the SQLite connection prefix
    path = SQLITE_PATH.split("///")[-1]
    # Remove any query parameters
    path = path.split("?")[0]
    return path

# Database file path
DB_FILE_PATH = get_sqlite_path()

# Lock for thread-safe operations
db_lock = threading.RLock()

def secure_db_file() -> None:
    """
    Secure the SQLite database file by setting appropriate permissions.
    
    This function sets the file permissions to be readable and writable
    only by the owner (600).
    """
    db_path = Path(DB_FILE_PATH)
    
    if not db_path.exists():
        logger.warning(f"Database file {DB_FILE_PATH} does not exist yet")
        return
    
    try:
        # Set file permissions to 600 (owner read/write only)
        os.chmod(DB_FILE_PATH, stat.S_IRUSR | stat.S_IWUSR)
        logger.info(f"Set secure permissions on database file {DB_FILE_PATH}")
    except Exception as e:
        logger.error(f"Failed to set secure permissions on database file: {e}")

def create_secure_directory(directory_path: str) -> None:
    """
    Create a secure directory for the database with appropriate permissions.
    
    Args:
        directory_path: The path to the directory to create
    """
    dir_path = Path(directory_path)
    
    if not dir_path.exists():
        try:
            # Create directory with secure permissions (700)
            dir_path.mkdir(parents=True, exist_ok=True)
            os.chmod(directory_path, stat.S_IRWXU)
            logger.info(f"Created secure directory {directory_path}")
        except Exception as e:
            logger.error(f"Failed to create secure directory: {e}")
    else:
        try:
            # Set secure permissions on existing directory
            os.chmod(directory_path, stat.S_IRWXU)
            logger.info(f"Set secure permissions on directory {directory_path}")
        except Exception as e:
            logger.error(f"Failed to set secure permissions on directory: {e}")

def backup_database() -> bool:
    """
    Create a secure backup of the database.
    
    Returns:
        True if backup was successful, False otherwise
    """
    db_path = Path(DB_FILE_PATH)
    
    if not db_path.exists():
        logger.warning(f"Database file {DB_FILE_PATH} does not exist, no backup needed")
        return False
    
    backup_path = f"{DB_FILE_PATH}.backup"
    
    try:
        with db_lock:
            # Create a backup copy
            shutil.copy2(DB_FILE_PATH, backup_path)
            # Set secure permissions on backup
            os.chmod(backup_path, stat.S_IRUSR | stat.S_IWUSR)
            logger.info(f"Created secure backup of database at {backup_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to create database backup: {e}")
        return False

def encrypt_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Encrypt sensitive fields in a data dictionary.
    
    Args:
        data: Dictionary containing data to encrypt
        
    Returns:
        Dictionary with sensitive fields encrypted
    """
    # Define fields that should be encrypted
    sensitive_fields = [
        "password", "api_key", "secret", "token", "credential",
        "private_key", "secret_key", "access_key"
    ]
    
    encrypted_data = data.copy()
    
    for field in sensitive_fields:
        if field in encrypted_data and encrypted_data[field]:
            # Encrypt the field value
            try:
                encrypted_value = encrypt_text(str(encrypted_data[field]))
                # Store as hex string for easier storage
                encrypted_data[f"{field}_enc"] = encrypted_value.hex()
                # Remove the original field
                del encrypted_data[field]
            except Exception as e:
                logger.error(f"Failed to encrypt field {field}: {e}")
    
    return encrypted_data

def decrypt_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decrypt sensitive fields in a data dictionary.
    
    Args:
        data: Dictionary containing encrypted data
        
    Returns:
        Dictionary with sensitive fields decrypted
    """
    decrypted_data = data.copy()
    
    # Find all encrypted fields
    encrypted_fields = [f for f in decrypted_data.keys() if f.endswith("_enc")]
    
    for field in encrypted_fields:
        try:
            # Get the original field name
            original_field = field[:-4]  # Remove "_enc" suffix
            # Decrypt the field value
            encrypted_value = bytes.fromhex(str(decrypted_data[field]))
            decrypted_value = decrypt_text(encrypted_value)
            # Add the decrypted field
            decrypted_data[original_field] = decrypted_value
            # Remove the encrypted field
            del decrypted_data[field]
        except Exception as e:
            logger.error(f"Failed to decrypt field {field}: {e}")
    
    return decrypted_data

@contextmanager
def secure_connection(pragmas: Optional[Dict[str, Any]] = None):
    """
    Create a secure SQLite connection with appropriate pragmas.
    
    Args:
        pragmas: Optional dictionary of pragmas to set
        
    Yields:
        A secure SQLite connection
    """
    # Default security pragmas
    default_pragmas = {
        "journal_mode": "WAL",  # Write-Ahead Logging for better concurrency
        "synchronous": "NORMAL",  # Balance between safety and performance
        "foreign_keys": "ON",  # Enforce foreign key constraints
        "secure_delete": "ON",  # Overwrite deleted data with zeros
        "auto_vacuum": "FULL",  # Automatically vacuum the database
    }
    
    # Combine default pragmas with any provided pragmas
    all_pragmas = {**default_pragmas, **(pragmas or {})}
    
    # Create a secure directory for the database if needed
    db_dir = os.path.dirname(DB_FILE_PATH)
    if db_dir:
        create_secure_directory(db_dir)
    
    connection = None
    try:
        with db_lock:
            # Create connection
            connection = sqlite3.connect(DB_FILE_PATH)
            
            # Set pragmas for security
            cursor = connection.cursor()
            for pragma, value in all_pragmas.items():
                cursor.execute(f"PRAGMA {pragma} = {value};")
            
            # Set secure file permissions
            secure_db_file()
            
            # Yield the connection
            yield connection
    finally:
        # Ensure connection is closed
        if connection:
            connection.close()

def initialize_db_security() -> None:
    """
    Initialize database security measures.
    
    This function should be called during application startup.
    """
    logger.info("Initializing database security measures")
    
    # Create a secure directory for the database
    db_dir = os.path.dirname(DB_FILE_PATH)
    if db_dir:
        create_secure_directory(db_dir)
    
    # Set secure permissions on the database file if it exists
    secure_db_file()
    
    # Create a backup if the database exists
    backup_database()
    
    logger.info("Database security measures initialized")
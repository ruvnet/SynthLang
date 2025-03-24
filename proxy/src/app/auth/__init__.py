"""
Authentication and authorization for the SynthLang Proxy.

This package provides functions for API key authentication, rate limiting,
and role-based access control.
"""
import asyncio
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Import from the original api_keys module
from .api_keys import (
    verify_api_key,
    get_user_id,
    get_rate_limit,
    check_rate_limit,
    allow_request,
    API_KEYS,
    _request_counts
)

# Import role-based access control functions
from .roles import (
    init_user_roles,
    get_user_roles,
    has_role,
    add_user_role,
    remove_user_role,
    require_role,
    USER_ROLES,
    DEFAULT_ROLES,
    ROLE_HIERARCHY
)

# Import database authentication functions
from .db_auth import (
    load_api_keys_from_db,
    API_KEY_CACHE
)

# Don't initialize roles when the module is imported
# This will be done properly in the lifespan function in main.py
# init_user_roles()
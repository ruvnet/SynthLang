# Role-Based Access Control System

## Overview

The Role-Based Access Control (RBAC) system in SynthLang Proxy provides a flexible and secure way to manage user permissions. It enables fine-grained control over which users can access specific features, tools, and resources within the application.

## Key Concepts

### Roles

Roles are named collections of permissions that can be assigned to users. The system includes a hierarchical role structure where higher-level roles inherit all permissions from lower-level roles.

Default roles in the system:

- **basic**: Default role assigned to all users
- **premium**: Enhanced access with additional features
- **admin**: Administrative access with system management capabilities

### Role Hierarchy

The role hierarchy defines the inheritance relationship between roles:

```
admin → premium → basic
```

This means:
- Users with the `admin` role automatically have all permissions of `premium` and `basic` roles
- Users with the `premium` role automatically have all permissions of the `basic` role
- The `basic` role is the foundation that all users have by default

## Configuration

### Environment Variables

The RBAC system can be configured using environment variables:

- `ADMIN_USERS`: Comma-separated list of user IDs with admin role
- `PREMIUM_USERS`: Comma-separated list of user IDs with premium role
- `DEFAULT_ROLE`: Default role assigned to users (default: "basic")

Example:
```
ADMIN_USERS=user1,user2
PREMIUM_USERS=user3,user4,user5
DEFAULT_ROLE=basic
```

### Role Definitions

Roles are defined in the system with their inheritance relationships:

```python
ROLE_HIERARCHY = {
    "admin": ["premium"],
    "premium": ["basic"],
    "basic": []
}

DEFAULT_ROLES = ["basic"]
```

## Usage

### Checking User Roles

To check if a user has a specific role:

```python
from app.auth.roles import has_role

if has_role("user123", "premium"):
    # Allow premium features
else:
    # Restrict to basic features
```

### Getting All User Roles

To get all roles assigned to a user (including inherited roles):

```python
from app.auth.roles import get_user_roles

roles = get_user_roles("user123")
# roles might be ["admin", "premium", "basic"] for an admin user
```

### Role-Based Decorators

The system provides decorators to restrict access to functions based on roles:

```python
from app.auth.roles import require_role

@require_role("admin")
async def admin_only_function(user_id):
    """This function can only be called by users with the admin role."""
    # Implementation...
    return "Admin function executed"
```

### Managing User Roles

To add a role to a user:

```python
from app.auth.roles import add_user_role

add_user_role("user123", "premium")
```

To remove a role from a user:

```python
from app.auth.roles import remove_user_role

remove_user_role("user123", "premium")
```

## Integration with Other Systems

### API Endpoint Protection

The RBAC system integrates with API endpoints to restrict access based on roles:

```python
@app.post("/admin/settings")
async def update_settings(request: Request, settings: SettingsModel):
    # Get the user ID from the request
    user_id = get_user_id_from_request(request)
    
    # Check if the user has the admin role
    if not has_role(user_id, "admin"):
        raise HTTPException(status_code=403, detail="Admin role required")
    
    # Process the request
    # ...
```

### Tool Access Control

The RBAC system integrates with the tool registry to restrict access to specific tools:

```python
from app.agents.registry import register_tool
from app.auth.roles import require_role

@require_role("premium")
async def premium_only_tool(param1, param2, user_id=None):
    """This tool can only be used by premium users."""
    # Implementation...
    return {"content": "Premium tool executed"}

# Register the tool
register_tool("premium_tool", premium_only_tool)
```

### Keyword Pattern Restrictions

The RBAC system integrates with the Keyword Detection System to restrict pattern matching based on roles:

```python
from app.keywords.registry import KeywordPattern, register_pattern

# Create a pattern that requires the admin role
admin_pattern = KeywordPattern(
    name="admin_action",
    pattern=r"(?:admin|system|configure|setup|manage)\s+(?:the|this)?\s*(?:system|server|application|app|service)\s+(?:to|for)?\s+(?P<action>.+)",
    tool="system_admin",
    description="Detects requests for system administration tasks",
    priority=200,
    required_role="admin"  # This pattern will only match for users with the admin role
)

# Register the pattern
register_pattern(admin_pattern)
```

## Security Considerations

### Role Assignment

- Roles should be assigned based on the principle of least privilege
- Admin roles should be limited to trusted users only
- Role assignments should be regularly audited

### Role Verification

- Always verify roles before allowing access to sensitive operations
- Use the `has_role` function or `require_role` decorator for consistent enforcement
- Never rely on client-side role verification

### Role Persistence

- User roles are stored in memory and initialized from environment variables
- For production systems, consider implementing a database-backed role storage system
- Implement proper backup and recovery procedures for role assignments

## Example Scenarios

### Multi-Tier Service Levels

Implementing different service tiers with role-based access:

```python
# Define tools with different access levels
@require_role("basic")
async def basic_search(query, user_id=None):
    """Basic search with limited results."""
    return {"content": "Basic search results (limited to 10)"}

@require_role("premium")
async def premium_search(query, user_id=None):
    """Premium search with more comprehensive results."""
    return {"content": "Premium search results (unlimited)"}

@require_role("admin")
async def admin_search(query, user_id=None):
    """Admin search with full access to all data."""
    return {"content": "Admin search results (full data access)"}

# Register the tools
register_tool("basic_search", basic_search)
register_tool("premium_search", premium_search)
register_tool("admin_search", admin_search)
```

### Feature Gating

Restricting access to beta features based on roles:

```python
@app.post("/v1/beta/features")
async def access_beta_features(request: Request):
    # Get the user ID from the request
    user_id = get_user_id_from_request(request)
    
    # Check if the user has the premium role (beta testers)
    if not has_role(user_id, "premium"):
        raise HTTPException(
            status_code=403, 
            detail="This feature is currently in beta and available only to premium users"
        )
    
    # Process the beta feature request
    # ...
```

## Extending the System

### Adding Custom Roles

To add a new role to the hierarchy:

```python
from app.auth.roles import ROLE_HIERARCHY

# Add a new "developer" role that inherits from "premium"
ROLE_HIERARCHY["developer"] = ["premium"]

# Now users with the "developer" role will also have "premium" and "basic" permissions
```

### Implementing Role-Based Metrics

Track usage patterns by role:

```python
from app.auth.roles import get_user_roles

async def track_request_metrics(user_id, endpoint, response_time):
    """Track API usage metrics by role."""
    roles = get_user_roles(user_id)
    
    # Record metrics for each role the user has
    for role in roles:
        await metrics.increment(f"api.requests.by_role.{role}")
        await metrics.record(f"api.response_time.by_role.{role}", response_time)
```

## Performance Considerations

- Role checks are performed in-memory for fast access
- Role inheritance is pre-computed when roles are assigned
- The system is designed to minimize the performance impact of role checks
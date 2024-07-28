from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Read schema for User model."""


class UserCreate(schemas.BaseUserCreate):
    """Create schema for User model."""


class UserUpdate(schemas.BaseUserUpdate):
    """Update schema for User model."""

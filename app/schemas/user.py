from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Read schema for User model."""

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'email': 'testUser@example.com',
                'is_active': True,
                'is_superuser': False,
                'is_verified': False
            }
        }


class UserCreate(schemas.BaseUserCreate):
    """Create schema for User model."""

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'email': 'testUser@example.com',
                'is_active': True,
                'is_superuser': False,
                'is_verified': False
            }
        }


class UserUpdate(schemas.BaseUserUpdate):
    """Update schema for User model."""

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'email': 'testUser@example.com',
                'is_active': True,
                'is_superuser': False,
                'is_verified': False
            }
        }

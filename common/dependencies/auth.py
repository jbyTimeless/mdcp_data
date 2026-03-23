from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from common.dependencies.database import get_db
from services.dataset.infrastructure.models import SysUser
from sqlalchemy import select

# This is a dummy/simplified dependency to extract the current user from context.
# In a real application, this would decode a JWT token or session cookie.
async def get_current_user(
    # e.g., token: str = Depends(oauth2_scheme),
    user_id: int = 666, # Mocking a user ID for demonstration
    db: AsyncSession = Depends(get_db)
) -> SysUser:
    # Simulating fetching the user by ID
    stmt = select(SysUser).where(SysUser.id == user_id, SysUser.is_deleted == 0)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    # If the user does not exist in the mock scenario, we create a mock user object
    if not user:
        # NOTE: Ideally this raises an HTTPException(status_code=401, detail="Unauthorized")
        # Creating a mock user to satisfy the context requirement for this exercise
        user = SysUser(
            id=1,
            user_id=10001,
            account="admin",
            username="Admin User",
            access_key="mock_ak",
            secret_key="mock_sk",
            role_code="admin"
        )
    return user

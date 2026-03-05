from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import BadRequestError, UnauthorizedError
from app.auth.security import create_access_token, hash_password, verify_password
from app.models.user_models import User
from app.schemas.auth_schemas import TokenResponse
from app.schemas.user_schemas import UserCreate, UserResponse


async def register(db: AsyncSession, user_create: UserCreate) -> UserResponse:
    """Register a new user with hashed password."""
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == user_create.email))
    if result.scalar_one_or_none() is not None:
        raise BadRequestError(detail="A user with this email already exists")

    # Check if username already exists
    result = await db.execute(select(User).where(User.username == user_create.username))
    if result.scalar_one_or_none() is not None:
        raise BadRequestError(detail="A user with this username already exists")

    # Create the user
    user = User(
        email=user_create.email,
        username=user_create.username,
        hashed_password=hash_password(user_create.password),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    return UserResponse.model_validate(user)


async def login(db: AsyncSession, email: str, password: str) -> TokenResponse:
    """Authenticate a user and return an access token."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(password, user.hashed_password):
        raise UnauthorizedError(detail="Invalid email or password")

    if not user.is_active:
        raise UnauthorizedError(detail="Account is deactivated")

    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token)

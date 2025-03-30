from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_get_db
from .models import User
from .schemas import UserCreateModel
from .utils import generate_passwd_hash
from typing import Optional


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession = Depends(async_get_db)) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalars().first()

    async def user_exists(self, email: str, session: AsyncSession = Depends(async_get_db)) -> bool:
        return await self.get_user_by_email(email, session) is not None

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession = Depends(async_get_db)) -> User:
        user_data_dict = user_data.model_dump()
        user_data_dict["password_hash"] = generate_passwd_hash(
            user_data_dict.pop("password"))
        new_user = User(**user_data_dict)
        session.add(new_user)
        await session.commit()
        # Ensure we return the updated instance
        await session.refresh(new_user)
        return new_user

    async def update_user(self, user: User, user_data: dict, session: AsyncSession = Depends(async_get_db)) -> User:
        for key, value in user_data.items():
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)  # Refresh instance after commit
        return user


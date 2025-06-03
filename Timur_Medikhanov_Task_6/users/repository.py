from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from .schemas import UserCreate, AdminCreate
from .models import User, Role


class RepositoryUser:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def create_user(self, user_in: UserCreate, hashed_password: str) -> User:
        new_user = User(
            username=user_in.username,
            password=hashed_password,
            role=Role.user,
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def create_admin(self, admin_in: AdminCreate, hashed_password: str) -> User:
        new_admin = User(
            username=admin_in.username,
            password=hashed_password,
            role=Role.admin,
        )
        self.session.add(new_admin)
        await self.session.commit()
        return new_admin

    async def get_user_by_username(self, username: str) -> User:
        users = select(User).where(username == User.username)
        result: Result = await self.session.execute(users)
        return result.scalars().one_or_none()

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.session.get(User, user_id)

    async def get_list_users(self) -> list[User]:
        stmt = select(User).where(User.role == Role.user)
        result: Result = await self.session.execute(stmt)
        return result.scalars().all()

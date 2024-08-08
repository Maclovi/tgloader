from sqlalchemy import Row, exc, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from loader.adapters.database.models import file, user
from loader.domain.common import Status
from loader.domain.models import File, User
from loader.domain.protocols import (
    FileMapperProtocol,
    UserMapperProtocol,
)


class Session:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _add_if_not_exists(self, obj: User | File) -> bool:
        try:
            self.session.add(obj)
            await self.session.commit()
            return True
        except exc.IntegrityError:
            await self.session.rollback()
            return False


class UserMapper(Session, UserMapperProtocol):
    def _load_user(self, row: Row) -> User:
        return User(
            id=row.id,
            first_name=row.first_name,
            last_name=row.last_name,
            username=row.username,
            status=row.status,
        )

    async def add_user(self, user: User) -> None:
        await self._add_if_not_exists(user)

    async def get_user_by_id(self, id: int) -> User | None:
        stmt = select(user).where(user.c.id == id)
        row = (await self.session.execute(stmt)).one_or_none()

        return self._load_user(row) if row else None

    async def update_user_status(self, id: int, new_status: Status) -> None:
        stmt = update(user).where(user.c.id == id).values(status=new_status)
        await self.session.execute(stmt)
        await self.session.commit()


class FileMapper(Session, FileMapperProtocol):
    def _load_file(self, row: Row) -> File:
        return File(
            video_id=row.video_id,
            file_id=row.file_id,
            message_id=row.message_id,
        )

    async def add_file(self, file: File) -> None:
        await self._add_if_not_exists(file)

    async def get_file_by_video_id(self, video_id: str) -> File | None:
        stmt = select(file).where(file.c.video_id == video_id)
        row = (await self.session.execute(stmt)).one_or_none()

        return self._load_file(row) if row else None


class DatabaseGateway(UserMapper, FileMapper):
    pass

from sqlalchemy import Row, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from loader.adapters.database.models import file, user
from loader.domain.models import File, User, UserFile
from loader.domain.protocols import (
    FileMapperProtocol,
    UserFileMapperProtocol,
    UserMapperProtocol,
)


class Session:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class UserMapper(Session, UserMapperProtocol):
    def _load_user(self, row: Row) -> User:
        return User(*row)

    async def add_user(self, user: User) -> None:
        self.session.add(user)

    async def get_user_by_id(self, id: int) -> User | None:
        stmt = select(user).where(user.c.id == id)
        row = (await self.session.execute(stmt)).one_or_none()

        return self._load_user(row) if row else None

    async def update_user(self, domain_user: "User", /) -> None:
        stmt = (
            update(user)
            .where(user.c.id == domain_user.id)
            .values(
                first_name=domain_user.first_name,
                last_name=domain_user.last_name,
                username=domain_user.username,
                status=domain_user.status,
            )
        )
        await self.session.execute(stmt)


class FileMapper(Session, FileMapperProtocol):
    def _load_file(self, row: Row) -> File:
        return File(*row)

    async def add_file(self, file: File) -> None:
        self.session.add(file)

    async def get_file_by_videoid(self, video_id: str) -> File | None:
        stmt = select(file).where(file.c.video_id == video_id)
        row = (await self.session.execute(stmt)).one_or_none()

        return self._load_file(row) if row else None


class UserFileMapper(Session, UserFileMapperProtocol):
    def _load_userfile(self, row: Row) -> UserFile:
        return UserFile(*row)

    async def add_userfile(self, userfile: UserFile) -> None:
        self.session.add(userfile)


class DatabaseGateway(UserMapper, FileMapper, UserFileMapper): ...

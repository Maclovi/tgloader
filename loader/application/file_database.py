from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

if TYPE_CHECKING:
    from loader.adapters.database.gateway import DatabaseGateway
    from loader.domain.models import File


class FileDatabase:
    def __init__(self, database: "DatabaseGateway") -> None:
        self.database = database

    async def create_file(self, file: "File") -> None:
        try:
            await self.database.add_file(file)
            await self.database.session.commit()
        except IntegrityError:
            await self.database.session.rollback()

    async def get_file_by_videoid(self, videoid: str) -> "File | None":
        return await self.database.get_file_by_videoid(videoid)

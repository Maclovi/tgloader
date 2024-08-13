from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from loader.domain.models import File

if TYPE_CHECKING:
    from loader.adapters.database.gateway import DatabaseGateway


class FileDatabase:
    def __init__(self, database: "DatabaseGateway") -> None:
        self.database = database

    async def create_file(self, videoid: str, fileid: str, msgid: int) -> None:
        file = File(video_id=videoid, file_id=fileid, message_id=msgid)
        try:
            await self.database.add_file(file)
            await self.database.session.commit()
        except IntegrityError:
            await self.database.session.rollback()

    async def get_file_by_videoid(self, videoid: str) -> "File | None":
        return await self.database.get_file_by_videoid(videoid)

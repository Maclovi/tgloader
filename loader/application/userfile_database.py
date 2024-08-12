from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

if TYPE_CHECKING:
    from loader.adapters.database.gateway import DatabaseGateway
    from loader.domain.models import UserFile


class UserFileDatabase:
    def __init__(self, database: "DatabaseGateway") -> None:
        self.database = database

    async def create_userfile(self, userfile: "UserFile") -> None:
        try:
            await self.database.add_userfile(userfile)
            await self.database.session.commit()
        except IntegrityError:
            await self.database.session.rollback()

from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from loader.domain.models import UserFile

if TYPE_CHECKING:
    from loader.adapters.database.gateway import DatabaseGateway


class UserFileDatabase:
    def __init__(self, database: "DatabaseGateway") -> None:
        self.database = database

    async def create_userfile(self, user_fk: int, file_fk: str) -> None:
        userfile = UserFile(user_fk, file_fk)
        try:
            await self.database.add_userfile(userfile)
            await self.database.session.commit()
        except IntegrityError:
            await self.database.session.rollback()

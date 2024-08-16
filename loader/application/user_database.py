from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

if TYPE_CHECKING:
    from loader.adapters.database.gateway import DatabaseGateway
    from loader.domain.models import User


class UserDatabase:
    def __init__(self, database: "DatabaseGateway") -> None:
        self.database = database

    async def create_user(self, user: "User") -> None:
        try:
            await self.database.add_user(user)
            await self.database.session.commit()
        except IntegrityError:
            await self.database.session.rollback()
            await self.database.update_user(user)
            await self.database.session.commit()

    async def update_user(self, user: "User") -> None:
        try:
            await self.database.update_user(user)
            await self.database.session.commit()
        except IntegrityError:
            await self.database.session.rollback()

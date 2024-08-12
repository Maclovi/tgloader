from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

from loader.domain.common import Status

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
            await self.database.update_user_status(user.id, "active")
            await self.database.session.commit()

    async def update_status(self, id: int, new_status: Status) -> None:
        await self.database.update_user_status(id, new_status)
        await self.database.session.commit()

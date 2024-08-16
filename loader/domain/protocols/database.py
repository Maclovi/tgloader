from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from loader.domain.models import File, User, UserFile


class UserMapperProtocol(Protocol):
    @abstractmethod
    async def add_user(self, user: "User") -> None: ...

    @abstractmethod
    async def update_user(self, user: "User", /) -> None: ...

    @abstractmethod
    async def get_user_by_id(self, id: int) -> "User | None": ...


class FileMapperProtocol(Protocol):
    @abstractmethod
    async def add_file(self, file: "File") -> None: ...

    @abstractmethod
    async def get_file_by_videoid(self, video_id: str) -> "File | None": ...


class UserFileMapperProtocol(Protocol):
    @abstractmethod
    async def add_userfile(self, userfile: "UserFile") -> None: ...


class DatabaseGatewayProtocol(
    UserMapperProtocol, FileMapperProtocol, UserFileMapperProtocol
): ...

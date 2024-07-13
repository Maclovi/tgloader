from abc import abstractmethod
from collections.abc import Iterable
from typing import Literal, Protocol, Self


class StreamProto(Protocol):
    def get_chunks(self, chunk_size: int | None = None) -> Iterable[bytes]:
        yield b""


class YouTubeProto(Protocol):
    url: str
    audio: StreamProto
    name: str
    thumb_url: str
    author: str
    file_size: int
    video_id: str
    duration: int
    views: int


class CommonDTOProto(Protocol):
    link: str
    message_ids: list[int]
    customer_user_id: int
    message_for_answer: str
    file_id: str
    status: Literal["ok", "bad"]
    error_info: str

    @abstractmethod
    def to_json(self) -> str: ...

    @classmethod
    @abstractmethod
    def to_dict(cls, raw_json: str | bytes | bytearray) -> Self: ...

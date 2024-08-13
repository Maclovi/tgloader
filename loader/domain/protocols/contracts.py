from abc import abstractmethod
from typing import Literal, Protocol, Self


class CommonDTOProto(Protocol):
    link: str
    customer_user_id: int
    message_ids: list[int]
    message_for_answer: str
    file_id: str
    status: Literal["ok", "bad"]
    error_info: str
    file_msg_id: int | None

    @abstractmethod
    def to_json(self) -> str: ...

    @classmethod
    @abstractmethod
    def to_dict(cls, raw_json: str | bytes | bytearray) -> Self: ...


class YouTubeSchemaProtocol(CommonDTOProto, Protocol):
    video_id: str

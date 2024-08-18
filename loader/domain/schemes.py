import json
import re
from dataclasses import dataclass
from typing import Literal, Self, TypeAlias

from .protocols import CommonDTOProto

JSONSerializedStr: TypeAlias = str


@dataclass(kw_only=True, order=True)
class BaseDTO(CommonDTOProto):
    link: str
    customer_user_id: int
    messages_cleanup: list[int]
    message_for_answer: str = ""
    file_id: str = ""
    status: Literal["ok", "bad"] = "ok"
    error_info: str = ""
    file_msg_id: int | None = None
    file_has_db: bool = False
    video_id: str = ""

    def __post_init__(self) -> None:
        if not self.message_for_answer:
            self.message_for_answer = f"<a href={self.link!r}>link</a>"

    def to_json(self) -> JSONSerializedStr:
        return json.dumps(self.__dict__)

    @classmethod
    def to_class(cls, raw_json: str | bytes | bytearray) -> Self:
        removed_prefix = cls._remove_prefix(raw_json)
        data = json.loads(removed_prefix)
        return cls(**data)

    @classmethod
    def _remove_prefix(cls, raw_json: str | bytes | bytearray) -> str:
        if isinstance(raw_json, bytes | bytearray):
            raw_json = raw_json.decode("uft-8")
        if not isinstance(raw_json, str):
            raise TypeError(f"Type {type(raw_json)} of raw_json is not str")

        return re.sub(r"^.+?(?=\[|\{)", "", raw_json, count=1)


@dataclass(kw_only=True)
class YouTubeDTO(BaseDTO):
    pass

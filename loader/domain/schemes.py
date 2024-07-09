import json
from dataclasses import dataclass
from typing import Literal, Self, TypeAlias

from .protocols import CommonDTOProto

JSONSerializedStr: TypeAlias = str


@dataclass(kw_only=True)
class BaseDTO(CommonDTOProto):
    link: str
    customer_user_id: int
    message_ids: list[int]
    link_html: str = ""
    file_id: str = ""
    error_info: str = ""
    status: Literal["ok", "bad"] = "ok"

    def __post_init__(self) -> None:
        if not self.link_html:
            self.link_html = f"<a href={self.link!r}>link</a>"

    def to_json(self) -> JSONSerializedStr:
        return json.dumps(self.__dict__)

    @classmethod
    def to_dict(cls, raw_json: str | bytes | bytearray) -> Self:
        data = json.loads(raw_json)
        return cls(**data)


@dataclass(kw_only=True)
class YouTubeDTO(BaseDTO):
    pass

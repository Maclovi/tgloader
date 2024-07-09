import json
from dataclasses import dataclass
from typing import Literal, TypeAlias

JSONSerializedStr: TypeAlias = str


@dataclass(kw_only=True)
class YouTubeDTO:
    customer_user_id: int
    message_ids: list[int]
    link: str
    link_html: str = ""
    file_id: str | None = None
    status: Literal["ok", "bad"] = "ok"
    error_info: str = "something went wrong, sorry, try later"

    def __post_init__(self) -> None:
        if not self.link_html:
            self.link_html = f"<a href={self.link!r}>link</a>"

    def to_json(self) -> JSONSerializedStr:
        return json.dumps(self.__dict__)

    @classmethod
    def to_dict(cls, raw_json: str | bytes | bytearray) -> "YouTubeDTO":
        data = json.loads(raw_json)
        return cls(**data)

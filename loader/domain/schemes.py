import json
from dataclasses import dataclass
from typing import Literal, TypeAlias

JSONSerializedStr: TypeAlias = str


@dataclass
class YouTubeDTO:
    customer_user_id: int
    link: str
    message_id: int
    file_id: str | None = None
    status: Literal["ok", "bad"] = "ok"
    error_info: str = "something went wrong, sorry"

    def dumps(self) -> JSONSerializedStr:
        return json.dumps(self.__dict__)

    @classmethod
    def to_dict(cls, raw_json: str | bytes | bytearray) -> "YouTubeDTO":
        data = json.loads(raw_json)
        return cls(**data)

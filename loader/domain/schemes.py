import json
from dataclasses import dataclass


@dataclass
class YouTubeDto:
    user_id: int
    link: str
    file_id: str | None = None

    def json_dumps(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, raw_json: str | bytes | bytearray) -> "YouTubeDto":
        data = json.loads(raw_json)
        return cls(**data)

from collections.abc import Iterable
from typing import Protocol


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

from collections.abc import Iterator
from typing import Protocol


class StreamProto(Protocol):
    @property
    def filesize(self) -> int: ...

    def iter_chunks(self, chunk_size: int | None = None) -> Iterator[bytes]:
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

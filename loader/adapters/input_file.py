from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

from aiogram.types.input_file import InputFile

from loader.domain.protocols import StreamProto, YouTubeProto

if TYPE_CHECKING:
    from aiogram.client.bot import Bot


class InputAudioTube:
    def __init__(
        self,
        audio: StreamProto,
        *,
        name: str | None = None,
        chunk_size: int = 9437184,  # 9mb.
    ) -> None:
        self.name = name
        self.chunk_size = chunk_size
        self.audio = audio.get_chunks(chunk_size)

    async def read(self, _: int) -> bytes:
        for chunk in self.audio:
            return chunk
        return b""


class YouTubeInputFile(InputFile):  # type: ignore
    def __init__(
        self,
        yt: YouTubeProto,
        filename: str | None = None,
        chunk_size: int = 9437184,  # 9mb.
    ) -> None:
        super().__init__(filename, chunk_size)
        self.audio = yt.audio.get_chunks(chunk_size)

    async def read(self, bot: "Bot") -> AsyncGenerator[bytes, None]:
        for chunk in self.audio:
            yield chunk

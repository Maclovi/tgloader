from logging import getLogger
from typing import TYPE_CHECKING, BinaryIO, NamedTuple, cast

from telethon.tl.types import DocumentAttributeAudio

from loader.adapters.input_file import InputAudioTube
from loader.adapters.youtube import YouTubeAdapter

if TYPE_CHECKING:
    from loader.domain.protocols.youtube import YouTubeProto
    from loader.ioc import Container

logger = getLogger(__name__)


class YouTubeMusicData(NamedTuple):
    ytube: "YouTubeProto"
    audio: BinaryIO
    audioattr: DocumentAttributeAudio
    thumb: bytes


async def get_music_data(link: str, ioc: "Container") -> YouTubeMusicData:
    ytube = YouTubeAdapter(link)
    audio = cast(
        BinaryIO, InputAudioTube(ytube.audio, name="n.mp3", chunk_size=524288)
    )
    audioattr = DocumentAttributeAudio(
        duration=ytube.duration,
        title=ytube.name,
        performer=ytube.author,
    )
    thumb = await (await ioc.http_client.get(ytube.thumb_url)).read()

    return YouTubeMusicData(ytube, audio, audioattr, thumb)

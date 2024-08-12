from dataclasses import dataclass
from typing import cast
from urllib.parse import urlparse

from pytubefix import YouTube
from pytubefix.streams import Stream

from loader.domain.protocols import YouTubeProto


@dataclass(slots=True)
class YouTubeAdapter(YouTubeProto):
    def __init__(
        self, url: str, auth: bool = True, cache_auth: bool = True
    ) -> None:
        yt = YouTube(url, use_oauth=auth, allow_oauth_cache=cache_auth)
        self.url = url
        self.audio = cast(Stream, yt.streams.get_audio_only())
        self.name = yt.title
        self.thumb_url = yt.thumbnail_url
        self.author = yt.author
        self.file_size = self.audio.filesize
        self.video_id = urlparse(url).query.split("=", 1)[-1]
        self.duration: int = yt.length
        self.views = yt.views

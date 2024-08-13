from typing import cast

from pytubefix import YouTube
from pytubefix.streams import Stream

from loader.domain.common import extract_video_id
from loader.domain.protocols import YouTubeProto


class YouTubeAdapter(YouTubeProto):
    __slots__ = (
        "url",
        "audio",
        "name",
        "thumb_url",
        "author",
        "file_size",
        "video_id",
        "duration",
        "views",
    )

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
        self.video_id = extract_video_id(url)
        self.duration: int = yt.length
        self.views = yt.views

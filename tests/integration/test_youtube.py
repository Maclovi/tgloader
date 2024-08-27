from collections.abc import Iterator
from pathlib import Path
from typing import cast

import pytest
from pytubefix import Stream, YouTube

from loader.adapters.youtube import YouTubeAdapter
from loader.auth import AuthYouTube
from loader.domain.common import extract_video_id


@pytest.fixture(scope="module", autouse=True)
def lifespan() -> Iterator[None]:
    AuthYouTube().auth()

    dir = Path("temp")
    Path.mkdir(dir, exist_ok=True)

    yield None

    for file in dir.iterdir():
        file.unlink()
    dir.rmdir()


@pytest.fixture
async def yt() -> YouTube:
    return YouTube(
        "https://www.youtube.com/watch?v=FiXCxfWWwPo", use_oauth=True
    )


@pytest.fixture
async def yta() -> YouTubeAdapter:
    return YouTubeAdapter("https://www.youtube.com/watch?v=FiXCxfWWwPo")


@pytest.mark.videoid
def test_extract_video_id() -> None:
    assert (
        extract_video_id("https://www.youtube.com/watch?v=FiXCxfWWwPo")
        == "FiXCxfWWwPo"
    )
    assert (
        extract_video_id("https://youtu.be/8B0fVk_ck2w?si=Ydhsadkjfhsdkj")
        == "8B0fVk_ck2w"
    )


@pytest.mark.youtube
class TestDownloadMp3:
    def test_download1(self, yt: "YouTube") -> None:
        audio = cast(Stream, yt.streams.get_audio_only())
        audio.download("temp")

    def test_download2(self, yta: "YouTubeAdapter") -> None:
        with Path("temp/temp2.mp3").open("wb") as file:
            file.writelines(yta.audio.iter_chunks())

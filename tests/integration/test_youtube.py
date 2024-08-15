from pathlib import Path
from typing import cast

import pytest
import pytubefix
from pytubefix import Stream, YouTube

from loader.adapters.youtube import YouTubeAdapter
from loader.domain.common import extract_video_id


def setup_module(_: pytest.Module) -> None:
    Path.mkdir(Path("temp"), exist_ok=True)


def teardown_module(_: pytest.Module) -> None:
    temp_dir = Path("temp")

    for file in temp_dir.iterdir():
        file.unlink()

    temp_dir.rmdir()


@pytest.fixture()
async def yt() -> YouTube:
    return YouTube("https://youtu.be/TCaNwAYqVI4?si=v4kdnDlg97csXjKN")


@pytest.fixture()
async def yta() -> YouTubeAdapter:
    return YouTubeAdapter("https://youtu.be/TCaNwAYqVI4?si=v4kdnDlg97csXjKN")


@pytest.mark.videoid()
def test_extract_video_id() -> None:
    assert (
        extract_video_id("https://www.youtube.com/watch?v=8B0fVk_ck2w&t=3s")
        == "8B0fVk_ck2w"
    )
    assert (
        extract_video_id("https://youtu.be/8B0fVk_ck2w?si=Ydhsadkjfhsdkj")
        == "8B0fVk_ck2w"
    )


@pytest.mark.skipif(
    pytubefix.__version__ == "6.11.0", reason="current version is tested"
)
@pytest.mark.download()
class TestDownloadMp3:
    def test_download1(self, yt: "YouTube") -> None:
        audio = cast(Stream, yt.streams.get_audio_only())
        audio.download("temp")

    def test_download2(self, yta: "YouTubeAdapter") -> None:
        with Path("temp/temp2.mp3").open("wb") as file:
            file.writelines(yta.audio.iter_chunks())

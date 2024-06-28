from pathlib import Path
from typing import Protocol


class AdapterYouTube(Protocol):
    async def download(self) -> str: ...

    def get_time(self) -> int: ...

    def get_path_file(self) -> Path: ...

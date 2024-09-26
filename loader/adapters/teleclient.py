from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telethon import TelegramClient

    from loader.application.youtube import YouTubeMusicData


class TelethonAdapter:
    def __init__(self, client: "TelegramClient", /) -> None:
        self._client = client

    async def send_audiotube(self, music: "YouTubeMusicData") -> None:
        """Do implemention"""
        pass

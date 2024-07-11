from typing import TYPE_CHECKING

from telethon import TelegramClient

if TYPE_CHECKING:
    from loader.config import TgClient


def get_client(client_config: "TgClient") -> TelegramClient:
    client = TelegramClient(
        "me",
        api_id=client_config.api_id,
        api_hash=client_config.api_hash,
        device_model="iPhone 11 Pro",
        system_version="IOS 100.1",
    )
    return client

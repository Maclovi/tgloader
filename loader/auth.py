import logging
import sys
from pathlib import Path

import pytube.auth
from pytube import YouTube

from loader.config import load_config
from loader.tgclient.client import get_client

logger = logging.getLogger(__name__)


def search_session_file() -> bool:
    return any(
        True
        for x in Path().iterdir()
        if x.is_file() and x.name.endswith(".session")
    )


def auth_youtube() -> None:
    if pytube.auth.is_auth():
        logger.info("__cache__ dir is exists")
        return

    _ = YouTube(
        "https://youtu.be/UprwkbzUX6g?si=pWBvtXGTlTMR8QLG",
        use_oauth=True,
        allow_oauth_cache=True,
    ).streams


def auth_telegram() -> None:
    if search_session_file():
        logger.info("Session file is exists")
        return

    client_config = load_config().tg_client
    client = get_client(client_config)
    with client:
        client.loop.run_until_complete(
            client.send_message("me", "hello, myself!")
        )


def auth_all() -> None:
    auth_youtube()
    auth_telegram()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    auth_all()

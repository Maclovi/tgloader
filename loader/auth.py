import logging
import shutil
import sys
from pathlib import Path

import pytube.auth
from pytube import YouTube

from loader.config import load_config
from loader.tgclient.client import get_client

logger = logging.getLogger(__name__)


def _auth_youtube() -> None:
    _ = YouTube(
        "https://youtu.be/UprwkbzUX6g?si=pWBvtXGTlTMR8QLG",
        use_oauth=True,
        allow_oauth_cache=True,
    ).streams


def auth_youtube() -> None:
    tokens = Path(".sens/tokens.json").resolve()
    path_yt = Path(pytube.auth.__file__).parent.resolve()
    if tokens.exists():
        logger.info("coping tokens.json to pytube dir base")
        (path_yt / "__cache__").mkdir()
        shutil.copy(tokens, path_yt / "__cache__/tokens.json")
    else:
        logger.info("Authorize user youtube account")
        _auth_youtube()


def _auth_telegram() -> None:
    client = get_client(conf.tg_client)
    with client:
        client.loop.run_until_complete(
            client.send_message("me", "hello, myself!")
        )


def auth_telegram() -> None:
    session_file = Path(".sens/me.session")
    if session_file.exists():
        logger.info("coping session file to base dir")
        shutil.copy(session_file, ".")
    else:
        logger.info("Authorize user telegram account")
        _auth_telegram()


def check_cache_pytube() -> bool:
    base = Path(pytube.auth.__file__).parent.resolve()
    return (base / "__cache__" / "tokens.json").exists()


def check_session_telegram() -> bool:
    return Path("me.session").resolve().exists()


def auth_all() -> None:
    if not check_cache_pytube():
        auth_youtube()
    if not check_session_telegram():
        auth_telegram()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    conf = load_config()
    auth_all()

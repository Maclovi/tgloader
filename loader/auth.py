import logging
import shutil
import sys
from pathlib import Path

import pytubefix

from loader.config import TgClient
from loader.ioc import init_container
from loader.tgclient.client import get_client

logger = logging.getLogger(__name__)


class AuthYouTube:
    def __init__(self) -> None:
        self.path_yt = Path(pytubefix.__file__).parent.resolve()

    def _auth(self) -> None:
        _ = pytubefix.YouTube(
            "https://youtu.be/UprwkbzUX6g?si=pWBvtXGTlTMR8QLG",
            use_oauth=True,
            allow_oauth_cache=True,
        ).streams

    def _auth_handler(self) -> None:
        tokens = Path(".sens/tokens.json").resolve()
        if tokens.exists() and self.path_yt:
            logger.info("coping tokens.json to pytube dir base")
            (self.path_yt / "__cache__").mkdir()
            shutil.copy(tokens, self.path_yt / "__cache__/tokens.json")
        else:
            logger.info("Authorize user youtube account")
            self._auth()

    def _check_cache_pytube(self) -> bool:
        return (self.path_yt / "__cache__" / "tokens.json").exists()

    def auth(self) -> None:
        if not self._check_cache_pytube():
            return self._auth_handler()

        logger.info("YouTube is authorized")


class AuthClient:
    def __init__(self, tg_client: TgClient) -> None:
        self.tg_client = tg_client

    def _auth(self) -> None:
        client = get_client(self.tg_client)
        with client:
            client.loop.run_until_complete(
                client.send_message("me", "hello, myself!")
            )

    def _auth_handler(self) -> None:
        session_file = Path(".sens/me.session")
        if session_file.exists():
            logger.info("coping session file to base dir")
            shutil.copy(session_file, ".")
        else:
            logger.info("Authorize user telegram account")
            self._auth()

    def _check_session_telegram(self) -> bool:
        return Path("me.session").resolve().exists()

    def auth(self) -> None:
        if not self._check_session_telegram():
            return self._auth_handler()

        logger.info("Client is authorized")


def auth_all() -> None:
    conf = init_container(resolve_httpclient=True).config
    AuthYouTube().auth()
    AuthClient(conf.tg_client).auth()


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    auth_all()


if __name__ == "__main__":
    main()

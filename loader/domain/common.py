from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging import Logger
from time import time
from typing import Literal, TypeAlias
from urllib.parse import urlparse

Status: TypeAlias = Literal["active", "inactive"]


@asynccontextmanager
async def timer(logger: Logger) -> AsyncIterator[None]:
    start = time()
    yield None
    logger.info(f"audio downloaded for {time() - start:.3f} seconds")


def extract_video_id(url: str) -> str:
    """
    Example: => https://www.youtube.com/watch?v=1Y2CD4WnbP0
    Extract to: => 1Y2CD4WnbP0
    """
    video_id = urlparse(url).query.split("=", 1)[-1]
    return video_id

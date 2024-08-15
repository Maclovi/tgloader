import re
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging import Logger
from time import time
from typing import Any, Literal, TypeAlias

Status: TypeAlias = Literal["active", "inactive"]


@asynccontextmanager
async def timer(logger: Logger) -> AsyncIterator[None]:
    start = time()
    yield None
    logger.info(f"audio downloaded for {time() - start:.3f} seconds")


def extract_video_id(url: str) -> str | Any:
    """
    Example: => https://www.youtube.com/watch?v=1Y2CD4WnbP0
    Extract to: => 1Y2CD4WnbP0
    """
    results = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if not results:
        raise TypeError("regex video_id is not found")
    return results.group(1)

from typing import cast

import pytest

from loader.ioc import Container


@pytest.mark.asyncio(scope="session")
async def test_redis_ping(ioc: Container) -> None:
    await ioc.redis.ping()


@pytest.mark.asyncio(scope="session")
async def test_redis_set(ioc: Container) -> None:
    await ioc.redis.set("key", "val")


@pytest.mark.asyncio(scope="session")
async def test_redis_get(ioc: Container) -> None:
    val = cast(bytes, (await ioc.redis.get("key"))).decode("utf8")
    assert val == "val"


@pytest.mark.asyncio(scope="session")
async def test_redis_delete(ioc: Container) -> None:
    await ioc.redis.delete("key")
    assert await ioc.redis.get("key") is None

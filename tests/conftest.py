from collections.abc import AsyncIterator

import pytest

from loader.ioc import Container, init_container


@pytest.fixture(scope="session")
async def ioc() -> AsyncIterator[Container]:
    cont = init_container()
    yield cont
    await cont.aclose()

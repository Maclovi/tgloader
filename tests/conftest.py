from typing import TYPE_CHECKING

import pytest

from loader.ioc import Container, init_container

if TYPE_CHECKING:
    from loader.config import Config


@pytest.fixture(scope="session")
def ioc() -> Container:
    return init_container()


@pytest.fixture(scope="session")
def config(ioc: Container) -> "Config":
    return ioc.config

from typing import TYPE_CHECKING, Literal, TypeAlias, cast

import pytest

from loader.ioc import Container, init_container

if TYPE_CHECKING:
    from loader.config import Config

Env: TypeAlias = Literal["dev", "prod"]


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="my option: dev or prod",
        choices=["prod", "dev"],
    )


@pytest.fixture(scope="session")
def env(request: pytest.FixtureRequest) -> Env:
    return cast(Env, request.config.getoption("--env"))


@pytest.fixture(scope="session")
def ioc(_: Env) -> Container:
    return init_container()


@pytest.fixture(scope="session")
def config(ioc: Container) -> "Config":
    return ioc.config

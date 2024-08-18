import pytest

from loader.domain.schemes import BaseDTO


@pytest.fixture()
def dto() -> BaseDTO:
    return BaseDTO(
        link="dsada", customer_user_id=12345, messages_cleanup=[12345, 54321]
    )


def test_jsonloads(dto: BaseDTO) -> None:
    queue = "somequeue"
    js = dto.to_json()
    queue_with_js = queue + js
    assert BaseDTO.to_class(queue_with_js) == dto

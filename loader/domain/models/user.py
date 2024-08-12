from dataclasses import dataclass, field
from datetime import datetime

from loader.domain.common import Status


@dataclass(order=True)
class User:
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    status: Status
    created_at: datetime | None = field(compare=False, default=None)
    updated_at: datetime | None = field(compare=False, default=None)

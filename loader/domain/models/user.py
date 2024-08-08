from dataclasses import dataclass, field
from datetime import datetime


@dataclass(order=True)
class User:
    id: int
    first_name: str
    last_name: str
    username: str
    status: str
    created_at: datetime | None = field(compare=False, default=None)
    updated_at: datetime | None = field(compare=False, default=None)

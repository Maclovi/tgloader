from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    username: str
    status: str
    created_at: datetime
    updated_at: datetime

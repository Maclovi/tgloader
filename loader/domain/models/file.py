from dataclasses import dataclass, field
from datetime import datetime


@dataclass(order=True)
class File:
    video_id: str
    file_id: str
    message_id: int
    created_at: datetime = field(compare=False, default_factory=datetime.now)
    updated_at: datetime | None = field(compare=False, default=None)

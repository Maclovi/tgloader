from dataclasses import dataclass, field
from datetime import datetime


@dataclass(order=True)
class File:
    video_id: str
    file_id: str
    message_id: int
    created_at: datetime = field(init=False)
    updated_at: datetime = field(init=False)

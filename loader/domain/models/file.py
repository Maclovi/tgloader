from dataclasses import dataclass
from datetime import datetime


@dataclass
class File:
    video_id: str
    file_id: str
    message_id: int
    created_at: datetime
    updated_at: datetime

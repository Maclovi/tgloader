from dataclasses import dataclass


@dataclass
class UserFile:
    user_fk: int
    file_fk: str

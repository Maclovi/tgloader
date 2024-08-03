from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import registry

from loader.domain.models import File, User

mapper_registry = registry()


user = Table(
    "user_account",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(254)),
    Column("last_name", String(254)),
    Column("username", String(254)),
    Column("status", String(7)),
    Column("created_at", String),
    Column("updated_at", String),
)


file = Table(
    "file",
    mapper_registry.metadata,
    Column("video_id", String(254), primary_key=True),
    Column("file_id", String(254)),
    Column("message_id", Integer),
    Column("created_at", String),
    Column("updated_at", String),
)


mapper_registry.map_imperatively(User, user)
mapper_registry.map_imperatively(File, file)

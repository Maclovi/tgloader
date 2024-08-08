from sqlalchemy import Column, DateTime, Integer, String, Table, func
from sqlalchemy.orm import registry

from loader.domain.models import File, User

mapper_registry = registry()


user = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(256)),
    Column("last_name", String(256)),
    Column("username", String(256)),
    Column("status", String(8)),
    Column("created_at", DateTime, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, onupdate=func.current_timestamp()),
)


file = Table(
    "file",
    mapper_registry.metadata,
    Column("video_id", String(256), primary_key=True),
    Column("file_id", String(256), nullable=False),
    Column("message_id", Integer, nullable=False),
    Column("created_at", DateTime, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, onupdate=func.current_timestamp()),
)


mapper_registry.map_imperatively(User, user)
mapper_registry.map_imperatively(File, file)

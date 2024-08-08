from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
)
from sqlalchemy.orm import registry

from loader.domain.models import File, User, UserFile

mapper_registry = registry()


user = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(256)),
    Column("last_name", String(256)),
    Column("username", String(256)),
    Column("status", String(8)),
    Column(
        "created_at",
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False,
    ),
    Column("updated_at", DateTime, onupdate=func.current_timestamp()),
)


file = Table(
    "file",
    mapper_registry.metadata,
    Column("video_id", String(256), primary_key=True),
    Column("file_id", String(256), nullable=False, unique=True),
    Column("message_id", Integer, nullable=False, unique=True),
    Column(
        "created_at",
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False,
    ),
    Column("updated_at", DateTime, onupdate=func.current_timestamp()),
)

user_file = Table(
    "user_file",
    mapper_registry.metadata,
    Column(
        "user_fk", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "file_fk",
        ForeignKey("file.video_id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

mapper_registry.map_imperatively(User, user)
mapper_registry.map_imperatively(File, file)
mapper_registry.map_imperatively(UserFile, user_file)

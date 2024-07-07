import logging
import re
from collections.abc import Callable
from typing import TypeVar

from aiogram.filters import KICKED, MEMBER, ChatMemberUpdatedFilter
from aiogram.filters import CommandStart as CommandStart
from aiogram.filters import Filter
from aiogram.types import Message, User

from loader.main.config import load_config

logger = logging.getLogger(__name__)

IF_KICKED = ChatMemberUpdatedFilter(member_status_changed=KICKED)
IF_MEMBER = ChatMemberUpdatedFilter(member_status_changed=MEMBER)

F_Return = TypeVar("F_Return")


class BaseRegex(Filter):  # type: ignore
    def __init__(self, regex: str) -> None:
        self.pattern: re.Pattern[str] = re.compile(regex)

    def _execute(
        self,
        message: Message,
        func: Callable[..., F_Return],
        /,
    ) -> bool:
        """Wrapper above a regex expression"""
        if not message.text:
            return False

        result = func(self.pattern, message.text)

        if result:
            logger.debug(
                f"Client's message: {message.text} | "
                f"{func.__name__} regex: {result}"
            )
        return bool(result)


class RegexSearch(BaseRegex):
    async def __call__(self, message: Message) -> bool:
        return self._execute(message, re.search)


class RegexFullMatch(BaseRegex):
    async def __call__(self, message: Message) -> bool:
        return self._execute(message, re.fullmatch)


class IsClient(Filter):  # type: ignore
    async def __call__(self, message: Message) -> bool:
        if not isinstance(message.from_user, User):
            return False
        user = message.from_user
        return bool(user.id == load_config().tg_ids.client_id)

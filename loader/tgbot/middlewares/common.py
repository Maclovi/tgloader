import logging
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, cast

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

if TYPE_CHECKING:
    from loader.ioc import Container

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        msg = cast(Message, event)

        ioc: "Container" = data["ioc"]  # noqa: UP037
        client_id = ioc.config.tg_ids.client_id
        user = f"user{msg.chat.id}"
        userttl = await ioc.redis.ttl(user)

        if userttl > 0 and msg.chat.id != client_id:
            await msg.answer(f"Stop flooding, repeat after {userttl}")
            return

        await ioc.redis.set(user, "0", ex=15)
        logger.info(f"Do processing by {user}")
        return await handler(msg, data)

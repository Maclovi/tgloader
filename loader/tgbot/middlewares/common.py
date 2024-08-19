import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, cast

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, TelegramObject, User

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
        allowed_users = (ioc.config.tg_ids.client_id,)
        request_user_id = cast(User, msg.from_user).id

        if request_user_id in allowed_users or get_flag(data, "media") is None:
            return await handler(msg, data)

        redis_user_key = f"user{request_user_id}"

        if (userttl := await ioc.redis.ttl(redis_user_key)) > 0:
            answer = f"Request limit exceeded, please try again in {userttl}"
            bot_ans = await msg.answer(answer)

            await asyncio.sleep(15)
            await msg.delete()
            await bot_ans.delete()
            return

        logger.info(f"Do processing by {redis_user_key!r}")
        await ioc.redis.set(redis_user_key, "0", ex=15)
        return await handler(msg, data)

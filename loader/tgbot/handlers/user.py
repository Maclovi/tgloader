import logging

from aiogram import F, Router
from aiogram.types import ChatMemberUpdated, Message

from loader.domain.services.youtube import get_file

from ..filters.user import (
    IF_KICKED,
    IF_MEMBER,
    CommandStart,
    RegexFullMatch,
    RegexSearch,
)

logger = logging.getLogger(__name__)
router = Router()
router.message.filter(F.chat.type == "private")


@router.message(CommandStart())
async def proccess_cmd_start(message: Message) -> None:
    assert message.text is not None

    await message.answer("Hello")


@router.message(RegexFullMatch("Помощь🚒"))
async def send_info(message: Message) -> None:
    assert message.text is not None

    await message.answer(message.text)


@router.message(RegexFullMatch("Легально?⚠"))
async def send_about_legal(message: Message) -> None:
    assert message.text is not None

    await message.answer(message.text)


@router.message(RegexFullMatch("Свой бот🤖"))
async def send_info_own(message: Message) -> None:
    assert message.text is not None

    await message.answer(message.text)


@router.message(RegexFullMatch("Предсказания🎱"))
async def send_prediction(message: Message) -> None:
    assert message.text is not None

    await message.answer(message.text)


@router.message(RegexFullMatch("Ответ на вопрос🎱"))
async def send_ball_response(message: Message) -> None:
    assert message.text is not None

    await message.answer(message.text)


@router.message(RegexSearch(r"(?i)youtu(\.be|be\.com)"))
async def send_youtube_music(message: Message) -> None:
    assert message.text is not None
    url = message.text

    data = get_file(url)
    await message.answer_audio(audio=data.file, thumbnail=data.thumbnail)


@router.my_chat_member(IF_KICKED)
async def process_user_blocked_bot(event: ChatMemberUpdated) -> None:
    print("Съебался")


@router.my_chat_member(IF_MEMBER)
async def process_user_unblocked_bot(event: ChatMemberUpdated) -> None:
    await event.answer("Zdarov")


@router.message()
async def send_echo(message: Message) -> None:
    await message.answer("Мне не удалось вас понять :(")

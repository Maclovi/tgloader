from telethon import TelegramClient, events


async def echo(event: events.NewMessage.Event) -> None:
    print(event.raw_text)
    print(event.message.message)


def include_events_handlers(client: TelegramClient) -> None:
    client.add_event_handler(echo, events.NewMessage())

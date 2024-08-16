from aiohttp import ClientSession


class ClientSessionStub(ClientSession):
    def __init__(self) -> None:
        pass

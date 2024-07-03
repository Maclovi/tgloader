from abc import abstractmethod
from collections.abc import Iterable
from typing import Protocol


class YouTubeProto(Protocol):
    @abstractmethod
    def read(self, url: str) -> Iterable[bytes]: ...

from pathlib import Path


def is_auth() -> bool:
    path = (Path(__file__).parent / "__cache__").resolve()
    return path.exists()

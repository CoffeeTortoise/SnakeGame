from typing import Any


class SaveLoad:

    @staticmethod
    def save(path: str, value: Any) -> None:
        item: str = str(value)
        with open(path, 'w') as file:
            file.write(item)

    @staticmethod
    def load(path: str) -> str:
        with open(path, 'r') as file:
            value: str = file.read()
        return value


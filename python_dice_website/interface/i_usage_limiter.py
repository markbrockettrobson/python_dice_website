import abc

import typing


class IUsageLimiter(abc.ABC):
    @abc.abstractmethod
    def is_over_limit(self, python_dice_program: typing.List[str]) -> bool:
        pass

    @staticmethod
    def get_over_limit_message() -> str:
        pass

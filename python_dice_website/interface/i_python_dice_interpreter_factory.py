import abc

import python_dice


class IPythonDiceInterpreterFactory(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_interpreter() -> python_dice.PythonDiceInterpreter:
        pass

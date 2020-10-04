import typing

import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory
import python_dice_website.interface.i_usage_limiter as i_usage_limiter


class UsageLimiter(i_usage_limiter.IUsageLimiter):
    def __init__(
        self,
        max_cost: int,
        interpreter_factory: i_python_dice_interpreter_factory.IPythonDiceInterpreterFactory,
    ):
        self._interpreter_factory = interpreter_factory
        self._max_cost = max_cost

    def is_over_limit(self, python_dice_program: typing.List[str]) -> bool:
        cost = self._interpreter_factory.get_interpreter().get_estimated_cost(
            python_dice_program
        )
        print(self._max_cost, cost, self._max_cost <= cost)
        return self._max_cost < cost

    @staticmethod
    def get_over_limit_message() -> str:
        return (
            "Due to the computational cost of your program the python dice website has refused your request.\n"
            "This is typically due to having large number dice in a keep/drop calculation or an excessive number "
            "of normal dice with a high number of sides. \n"
            "You can run this simulation on your owen hardware with the open source code.\n"
            "For the python pip package python_dice see https://pypi.org/project/python-dice/"
            "and https://github.com/markbrockettrobson/python_dice .\n"
            "For deploying your own website see https://github.com/markbrockettrobson/python_dice_website ."
        )

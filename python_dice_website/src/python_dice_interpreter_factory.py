import python_dice

import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory


class PythonDiceInterpreterFactory(
    i_python_dice_interpreter_factory.IPythonDiceInterpreterFactory
):
    @staticmethod
    def get_interpreter() -> python_dice.PythonDiceInterpreter:
        return python_dice.PythonDiceInterpreter()

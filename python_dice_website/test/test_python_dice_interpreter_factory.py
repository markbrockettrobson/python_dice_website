import unittest

import python_dice

import python_dice_website.src.python_dice_interpreter_factory as python_dice_interpreter_factory


class TestPythonDiceInterpreterFactory(unittest.TestCase):
    def setUp(self) -> None:
        self._python_dice_interpreter_factory = (
            python_dice_interpreter_factory.PythonDiceInterpreterFactory()
        )

    def test_get_interpreter_type(self):
        interpreter = self._python_dice_interpreter_factory.get_interpreter()

        self.assertEqual(type(interpreter), python_dice.PythonDiceInterpreter)

    def test_get_interpreter_new_interpreter(self):
        interpreter_one = self._python_dice_interpreter_factory.get_interpreter()
        interpreter_two = self._python_dice_interpreter_factory.get_interpreter()

        self.assertNotEqual(interpreter_one, interpreter_two)

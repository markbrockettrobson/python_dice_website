import unittest
import unittest.mock as mock

import python_dice_website.src.usage_limiter as usage_limiter
import python_dice.interface.i_python_dice_interpreter as i_python_dice_interpreter
import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory


class TestUsageLimiter(unittest.TestCase):
    def setUp(self) -> None:
        self._mock_program = ["mock_program"]
        self._mock_python_dice_interpreter = mock.create_autospec(
            spec=i_python_dice_interpreter.IPythonDiceInterpreter,
            spec_set=True
        )
        self._mock_python_dice_interpreter.get_estimated_cost.return_value = 110000
        self._mock_python_dice_interpreter_factory = mock.create_autospec(
            spec=i_python_dice_interpreter_factory.IPythonDiceInterpreterFactory,
            spec_set=True
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.return_value = self._mock_python_dice_interpreter

        self._usage_limiter = usage_limiter.UsageLimiter(
            max_cost=100000,
            interpreter_factory=self._mock_python_dice_interpreter_factory
        )

    def test_is_over_limit_true(self):
        self.assertTrue(self._usage_limiter.is_over_limit(self._mock_program))
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_estimated_cost.assert_called_once_with(self._mock_program)

    def test_is_over_limit_false(self):
        self._mock_python_dice_interpreter.get_estimated_cost.return_value = 90000
        self.assertFalse(self._usage_limiter.is_over_limit(self._mock_program))
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_estimated_cost.assert_called_once_with(self._mock_program)

    def test_get_over_limit_message(self):
        self.assertGreater(len(self._usage_limiter.get_over_limit_message()), 2)
        self.assertEqual(type(self._usage_limiter.get_over_limit_message()), str)

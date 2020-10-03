import unittest
import unittest.mock as mock

import flask
import python_dice

import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory
import python_dice_website.src.python_dice_web_app_factory as python_dice_web_app_factory


class TestMaxAPI(unittest.TestCase):
    def setUp(self) -> None:
        self._mock_max = 12345

        self._mock_python_dice_interpreter = mock.create_autospec(
            spec=python_dice.PythonDiceInterpreter, spec_set=True
        )
        self._mock_python_dice_interpreter.max.return_value = {"stdout": self._mock_max}
        self._mock_python_dice_interpreter_factory = mock.create_autospec(
            spec=i_python_dice_interpreter_factory.IPythonDiceInterpreterFactory,
            spec_set=True,
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.return_value = (
            self._mock_python_dice_interpreter
        )

        self._test_app = (
            python_dice_web_app_factory.PythonDiceWebAppFactory.create_test_app(
                interpreter_factory=self._mock_python_dice_interpreter_factory
            )
            .get_app()
            .test_client()
        )

    def test_post(self):
        response = self._test_app.post(
            "/api/max",
            data=flask.json.dumps({"program": "1d2 + 3"}),
            content_type="application/json",
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.max.assert_called_once_with(["1d2 + 3"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), f"{self._mock_max}\n")

    def test_get(self):
        response = self._test_app.get("/api/max?program=2%20%2B%203d2")
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.max.assert_called_once_with(["2 + 3d2"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), f"{self._mock_max}\n")

    def test_error_post(self):
        self._mock_python_dice_interpreter.max.side_effect = ValueError("mock_error")
        response = self._test_app.post(
            "/api/max",
            data=flask.json.dumps({"program": "ABS(1 - 3d30"}),
            content_type="application/json",
        )

        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.max.assert_called_once_with(["ABS(1 - 3d30"])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), '"mock_error"\n')

    def test_error_get(self):
        self._mock_python_dice_interpreter.max.side_effect = ValueError("mock_error")
        response = self._test_app.get("/api/max?program=ABS%281%20%2D%203d30")

        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.max.assert_called_once_with(["ABS(1 - 3d30"])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), '"mock_error"\n')

    def test_post_no_program(self):
        response = self._test_app.post(
            "/api/max", data=flask.json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_data(as_text=True), f'"No program in request json."\n'
        )

    def test_get_no_program(self):
        response = self._test_app.get("/api/max")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_data(as_text=True), f'"No url parameter program."\n'
        )

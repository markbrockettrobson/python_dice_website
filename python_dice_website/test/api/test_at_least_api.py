import unittest
import unittest.mock as mock

import flask
import PIL.Image as Image
import python_dice

import python_dice_website.interface.i_pil_image_sender as i_pil_image_sender
import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory
import python_dice_website.src.python_dice_web_app_factory as python_dice_web_app_factory


class TestAtLeastAPI(unittest.TestCase):
    def setUp(self) -> None:
        self._mock_pill_image = mock.create_autospec(spec=Image, spec_set=True)
        self._mock_image_sender_return = "lets just say this is an image =)"

        self._mock_python_dice_interpreter = mock.create_autospec(
            spec=python_dice.PythonDiceInterpreter, spec_set=True
        )
        self._mock_python_dice_interpreter.get_at_least_histogram.return_value = (
            self._mock_pill_image
        )
        self._mock_python_dice_interpreter_factory = mock.create_autospec(
            spec=i_python_dice_interpreter_factory.IPythonDiceInterpreterFactory,
            spec_set=True,
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.return_value = (
            self._mock_python_dice_interpreter
        )

        self._mock_pil_image_sender = mock.create_autospec(
            spec=i_pil_image_sender.IPilImageSender, spec_set=True
        )
        self._mock_pil_image_sender.send_image.return_value = (
            self._mock_image_sender_return
        )

        self._test_app = (
            python_dice_web_app_factory.PythonDiceWebAppFactory.create_test_app(
                image_sender=self._mock_pil_image_sender,
                interpreter_factory=self._mock_python_dice_interpreter_factory,
            )
            .get_app()
            .test_client()
        )

    def test_post(self):
        response = self._test_app.post(
            "/api/at_least",
            data=flask.json.dumps({"program": "1 + 3"}),
            content_type="application/json",
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_at_least_histogram.assert_called_once_with(
            ["1 + 3"]
        )
        self._mock_pil_image_sender.send_image.assert_called_once_with(
            self._mock_pill_image
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True), f'"{self._mock_image_sender_return}"\n'
        )

    def test_get(self):
        response = self._test_app.get("/api/at_least?program=2%20%2B%203")
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_at_least_histogram.assert_called_once_with(
            ["2 + 3"]
        )
        self._mock_pil_image_sender.send_image.assert_called_once_with(
            self._mock_pill_image
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True), f'"{self._mock_image_sender_return}"\n'
        )

    def test_error_post(self):
        self._mock_python_dice_interpreter.get_at_least_histogram.side_effect = ValueError(
            "mock_error"
        )
        response = self._test_app.post(
            "/api/at_least",
            data=flask.json.dumps({"program": "ABS(1 - 3d30"}),
            content_type="application/json",
        )

        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_at_least_histogram.assert_called_once_with(
            ["ABS(1 - 3d30"]
        )
        self._mock_pil_image_sender.send_image.assert_not_called()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), '"mock_error"\n')

    def test_error_get(self):
        self._mock_python_dice_interpreter.get_at_least_histogram.side_effect = ValueError(
            "mock_error"
        )
        response = self._test_app.get("/api/at_least?program=ABS%281%20%2D%203d30")

        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_at_least_histogram.assert_called_once_with(
            ["ABS(1 - 3d30"]
        )
        self._mock_pil_image_sender.send_image.assert_not_called()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), '"mock_error"\n')

    def test_post_no_program(self):
        response = self._test_app.post(
            "/api/at_least", data=flask.json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_data(as_text=True), f'"No program in request json."\n'
        )

    def test_get_no_program(self):
        response = self._test_app.get("/api/at_least")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_data(as_text=True), f'"No url parameter program."\n'
        )

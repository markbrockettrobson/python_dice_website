import unittest
import unittest.mock as mock

import flask
import PIL.Image as Image
import python_dice

import python_dice_website.interface.i_pil_image_sender as i_pil_image_sender
import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory
import python_dice_website.src.python_dice_web_app_factory as python_dice_web_app_factory


class TestCompareAPI(unittest.TestCase):
    def setUp(self) -> None:
        self._mock_pill_image = mock.create_autospec(spec=Image, spec_set=True)
        self._mock_image_sender_return = "lets just say this is an image =)"
        self._mock_distribution_1 = mock.Mock()
        self._mock_distribution_2 = mock.Mock()
        self._mock_distribution_1.get_compare.return_value = self._mock_pill_image
        self._mock_python_dice_interpreter = mock.create_autospec(
            spec=python_dice.PythonDiceInterpreter, spec_set=True
        )
        self._mock_python_dice_interpreter.get_probability_distributions.side_effect = [
            {"stdout": self._mock_distribution_1},
            {"stdout": self._mock_distribution_2},
        ]
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
            "/api/compare",
            data=flask.json.dumps(
                {
                    "program_one": "10d6",
                    "program_two": "6d8 + 3",
                    "program_one_name": "Name one",
                    "program_two_name": "Name two",
                }
            ),
            content_type="application/json",
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_probability_distributions.assert_has_calls(
            [mock.call(["10d6"]), mock.call(["6d8 + 3"])]
        )
        self._mock_distribution_1.get_compare.assert_called_once_with(
            self._mock_distribution_2, "Name one", "Name two"
        )
        self._mock_pil_image_sender.send_image.assert_called_once_with(
            self._mock_pill_image
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True), f'"{self._mock_image_sender_return}"\n'
        )

    def test_post_no_names(self):
        response = self._test_app.post(
            "/api/compare",
            data=flask.json.dumps({"program_one": "10d6", "program_two": "6d8 + 3"}),
            content_type="application/json",
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_probability_distributions.assert_has_calls(
            [mock.call(["10d6"]), mock.call(["6d8 + 3"])]
        )
        self._mock_distribution_1.get_compare.assert_called_once_with(
            self._mock_distribution_2, "Program one", "Program two"
        )
        self._mock_pil_image_sender.send_image.assert_called_once_with(
            self._mock_pill_image
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True), f'"{self._mock_image_sender_return}"\n'
        )

    def test_post_no_name_one(self):
        response = self._test_app.post(
            "/api/compare",
            data=flask.json.dumps(
                {
                    "program_one": "10d6",
                    "program_two": "6d8 + 3",
                    "program_one_name": "Name one",
                }
            ),
            content_type="application/json",
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_probability_distributions.assert_has_calls(
            [mock.call(["10d6"]), mock.call(["6d8 + 3"])]
        )
        self._mock_distribution_1.get_compare.assert_called_once_with(
            self._mock_distribution_2, "Name one", "Program two"
        )
        self._mock_pil_image_sender.send_image.assert_called_once_with(
            self._mock_pill_image
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True), f'"{self._mock_image_sender_return}"\n'
        )

    def test_post_no_name_two(self):
        response = self._test_app.post(
            "/api/compare",
            data=flask.json.dumps(
                {
                    "program_one": "10d6",
                    "program_two": "6d8 + 3",
                    "program_two_name": "Name two",
                }
            ),
            content_type="application/json",
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_probability_distributions.assert_has_calls(
            [mock.call(["10d6"]), mock.call(["6d8 + 3"])]
        )
        self._mock_distribution_1.get_compare.assert_called_once_with(
            self._mock_distribution_2, "Program one", "Name two"
        )
        self._mock_pil_image_sender.send_image.assert_called_once_with(
            self._mock_pill_image
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True), f'"{self._mock_image_sender_return}"\n'
        )

    def test_get(self):
        response = self._test_app.get(
            "/api/compare?program_one=2d6&program_two=3d4&program_one_name=Name%20one&program_two_name=Name%20two"
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_probability_distributions.assert_has_calls(
            [mock.call(["2d6"]), mock.call(["3d4"])]
        )
        self._mock_distribution_1.get_compare.assert_called_once_with(
            self._mock_distribution_2, "Name one", "Name two"
        )
        self._mock_pil_image_sender.send_image.assert_called_once_with(
            self._mock_pill_image
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True), f'"{self._mock_image_sender_return}"\n'
        )

    def test_get_no_names(self):
        response = self._test_app.get("/api/compare?program_one=2d6&program_two=3d4")
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_probability_distributions.assert_has_calls(
            [mock.call(["2d6"]), mock.call(["3d4"])]
        )
        self._mock_distribution_1.get_compare.assert_called_once_with(
            self._mock_distribution_2, "Program one", "Program two"
        )
        self._mock_pil_image_sender.send_image.assert_called_once_with(
            self._mock_pill_image
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True), f'"{self._mock_image_sender_return}"\n'
        )

    def test_get_no_name_one(self):
        response = self._test_app.get(
            "/api/compare?program_one=2d6&program_two=3d4&program_two_name=Name%20two"
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_probability_distributions.assert_has_calls(
            [mock.call(["2d6"]), mock.call(["3d4"])]
        )
        self._mock_distribution_1.get_compare.assert_called_once_with(
            self._mock_distribution_2, "Program one", "Name two"
        )
        self._mock_pil_image_sender.send_image.assert_called_once_with(
            self._mock_pill_image
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True), f'"{self._mock_image_sender_return}"\n'
        )

    def test_get_name_two(self):
        response = self._test_app.get(
            "/api/compare?program_one=2d6&program_two=3d4&program_one_name=Name%20one"
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self._mock_python_dice_interpreter.get_probability_distributions.assert_has_calls(
            [mock.call(["2d6"]), mock.call(["3d4"])]
        )
        self._mock_distribution_1.get_compare.assert_called_once_with(
            self._mock_distribution_2, "Name one", "Program two"
        )
        self._mock_pil_image_sender.send_image.assert_called_once_with(
            self._mock_pill_image
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True), f'"{self._mock_image_sender_return}"\n'
        )

    def test_error_post(self):
        self._mock_python_dice_interpreter.get_probability_distributions.side_effect = ValueError(
            "mock_error"
        )
        response = self._test_app.post(
            "/api/compare",
            data=flask.json.dumps(
                {
                    "program_one": "10d6",
                    "program_two": "6d8 + 3",
                    "program_one_name": "Name one",
                    "program_two_name": "Name two",
                }
            ),
            content_type="application/json",
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), f'"mock_error"\n')

    def test_error_get(self):
        self._mock_python_dice_interpreter.get_probability_distributions.side_effect = ValueError(
            "mock_error"
        )
        response = self._test_app.get(
            "/api/compare?program_one=2d6&program_two=3d4&program_one_name=Name%20one&program_two_name=Name%20two"
        )
        self._mock_python_dice_interpreter_factory.get_interpreter.assert_called_once()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), f'"mock_error"\n')

    def test_post_no_programs(self):
        response = self._test_app.post(
            "/api/compare", data=flask.json.dumps({}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_data(as_text=True),
            f'"No json program_one and/or program_two."\n',
        )

    def test_post_no_program_one(self):
        response = self._test_app.post(
            "/api/compare",
            data=flask.json.dumps({"program_two": "6d8 + 3"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_data(as_text=True),
            f'"No json program_one and/or program_two."\n',
        )

    def test_post_no_program_two(self):
        response = self._test_app.post(
            "/api/compare",
            data=flask.json.dumps({"program_one": "10d6"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_data(as_text=True),
            f'"No json program_one and/or program_two."\n',
        )

    def test_get_no_programs(self):
        response = self._test_app.get("/api/compare")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_data(as_text=True), f'"No url parameter program_one."\n'
        )

    def test_get_no_program_one(self):
        response = self._test_app.get("/api/compare?program_two=3d4")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_data(as_text=True), f'"No url parameter program_one."\n'
        )

    def test_get_no_program_two(self):
        response = self._test_app.get("/api/compare?program_one=2d6")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_data(as_text=True), f'"No url parameter program_two."\n'
        )

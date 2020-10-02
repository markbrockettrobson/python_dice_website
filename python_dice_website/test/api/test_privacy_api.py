import unittest

import python_dice_website.src.python_dice_web_app_factory as python_dice_web_app_factory


class TestRollAPI(unittest.TestCase):
    def setUp(self) -> None:
        self._test_app = (
            python_dice_web_app_factory.PythonDiceWebAppFactory.create_test_app()
            .get_app()
            .test_client()
        )

    def test_privacy(self):
        response = self._test_app.get("/api/privacy")

        _ = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)

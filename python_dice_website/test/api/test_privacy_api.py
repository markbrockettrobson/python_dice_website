import unittest


import python_dice_website.src.app as app


class TestRollAPI(unittest.TestCase):
    def test_privacy(self):
        response = app.APP.test_client().get("/privacy")

        _ = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)

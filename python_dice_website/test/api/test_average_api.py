import unittest

import flask

import python_dice_website.src.app as app


class TestAverageAPI(unittest.TestCase):
    def test_add_post(self):
        response = app.APP.test_client().post(
            "/average",
            data=flask.json.dumps({"program": "1d2 + 3"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "4.5")

    def test_add_get(self):
        response = app.APP.test_client().get("/average?program=2%20%2B%203d2")

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "6.5")

    def test_sub_post(self):
        response = app.APP.test_client().post(
            "/average",
            data=flask.json.dumps({"program": "ABS(1d20 - 3)"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "7.8")

    def test_sub_get(self):
        response = app.APP.test_client().get("/average?program=2%20%2D%203d50")

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "-74.5")

    def test_error_post(self):
        response = app.APP.test_client().post(
            "/average",
            data=flask.json.dumps({"program": "ABS(1 - 3d30"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data, "Ran into a $end ($end) where it wasn't expected, at position None."
        )

    def test_error_get(self):
        response = app.APP.test_client().get("/average?program=ABS%281%20%2D%203d30")

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data, "Ran into a $end ($end) where it wasn't expected, at position None."
        )

    def test_error_two_post(self):
        response = app.APP.test_client().post(
            "/average",
            data=flask.json.dumps({"program": "3d3d0"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "(None, SourcePosition(idx=3, lineno=-1, colno=-1))")

    def test_error_two_get(self):
        response = app.APP.test_client().get("/average?program=3d3d0")

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "(None, SourcePosition(idx=3, lineno=-1, colno=-1))")

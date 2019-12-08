import unittest

import flask

import python_dice_website.src.app as app


class TestRollAPI(unittest.TestCase):
    def test_add(self):
        response = app.APP.test_client().post(
            "/roll",
            data=flask.json.dumps({"program": "1 + 3"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "4")

    def test_sub(self):
        response = app.APP.test_client().post(
            "/roll",
            data=flask.json.dumps({"program": "ABS(1 - 3)"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "2")

    def test_error(self):
        response = app.APP.test_client().post(
            "/roll",
            data=flask.json.dumps({"program": "ABS(1 - 3d30"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data, "Ran into a $end ($end) where it wasn't expected, at position None."
        )

    def test_error_two(self):
        response = app.APP.test_client().post(
            "/roll",
            data=flask.json.dumps({"program": "3d3d0"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "(None, SourcePosition(idx=3, lineno=-1, colno=-1))")

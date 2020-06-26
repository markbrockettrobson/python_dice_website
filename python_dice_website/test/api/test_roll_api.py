import unittest

import flask

import python_dice_website.src.app as app


class TestRollAPI(unittest.TestCase):
    def test_add_post(self):
        response = app.APP.test_client().post(
            "/roll",
            data=flask.json.dumps({"program": "1 + 3"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "4")

    def test_add_get(self):
        response = app.APP.test_client().get("/roll?program=2%20%2B%203")

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "5")

    def test_sub_post(self):
        response = app.APP.test_client().post(
            "/roll",
            data=flask.json.dumps({"program": "ABS(1 - 3)"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "2")

    def test_sub_get(self):
        response = app.APP.test_client().get("/roll?program=2%20%2D%203")

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "-1")

    def test_error_post(self):
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

    def test_error_get(self):
        response = app.APP.test_client().get("/roll?program=ABS%281%20%2D%203d30")

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data, "Ran into a $end ($end) where it wasn't expected, at position None."
        )

    def test_error_two_post(self):
        response = app.APP.test_client().post(
            "/roll",
            data=flask.json.dumps({"program": "3d3d1d0"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data,
            "Ran into a DICE (d0) where it wasn't expected, at position SourcePosition(idx=5, lineno=1, colno=6).",
        )

    def test_error_two_get(self):
        response = app.APP.test_client().get("/roll?program=3d3d1d0")

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data,
            "Ran into a DICE (d0) where it wasn't expected, at position SourcePosition(idx=5, lineno=1, colno=6).",
        )

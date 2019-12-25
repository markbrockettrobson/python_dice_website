import unittest

import flask

import python_dice_website.src.app as app


class TestAtLeastAPI(unittest.TestCase):
    def disable_test_add_post(self):
        response = app.APP.test_client().post(
            "/atleast",
            data=flask.json.dumps({"program": "1 + 3"}),
            content_type="application/json",
        )

        data = response.get_data()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data.decode("ISO-8859-1")), 18917)

    def disable_test_add_get(self):
        response = app.APP.test_client().get("/atleast?program=2%20%2B%203")

        data = response.get_data()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data.decode("ISO-8859-1")), 18973)

    def disable_test_sub_post(self):
        response = app.APP.test_client().post(
            "/atleast",
            data=flask.json.dumps({"program": "ABS(1 - 3)"}),
            content_type="application/json",
        )

        data = response.get_data()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data.decode("ISO-8859-1")), 18831)

    def disable_test_sub_get(self):
        response = app.APP.test_client().get("/atleast?program=2%20%2D%203")

        data = response.get_data()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data.decode("ISO-8859-1")), 18940)

    def disable_test_error_post(self):
        response = app.APP.test_client().post(
            "/atleast",
            data=flask.json.dumps({"program": "ABS(1 - 3d30"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data, "Ran into a $end ($end) where it wasn't expected, at position None."
        )

    def disable_test_error_get(self):
        response = app.APP.test_client().get("/atleast?program=ABS%281%20%2D%203d30")

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data, "Ran into a $end ($end) where it wasn't expected, at position None."
        )

    def disable_test_error_two_post(self):
        response = app.APP.test_client().post(
            "/atleast",
            data=flask.json.dumps({"program": "3d3d0"}),
            content_type="application/json",
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "(None, SourcePosition(idx=3, lineno=-1, colno=-1))")

    def disable_test_error_two_get(self):
        response = app.APP.test_client().get("/atleast?program=3d3d0")

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "(None, SourcePosition(idx=3, lineno=-1, colno=-1))")
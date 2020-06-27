import unittest

import python_dice_website.src.app as app


class TestRollAPI(unittest.TestCase):
    def test_add_post(self):
        response = app.APP.test_client().post("/slackroll", data=dict(text="1 + 3"))

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data,
            '{"blocks":[{"text":{"text":"1 + 3","type":"mrkdwn"},'
            '"type":"section"},{"text":{"text":"4","type":"mrkdwn"},"type":"section"}],"response_type":"in_channel"}\n',
        )

    def test_sub_post(self):
        response = app.APP.test_client().post(
            "/slackroll", data=dict(text="ABS(1 - 3)")
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data,
            '{"blocks":[{"text":{"text":"ABS(1 - 3)","type":"mrkdwn"},'
            '"type":"section"},{"text":{"text":"2","type":"mrkdwn"},"type":"section"}],"response_type":"in_channel"}\n',
        )

    def test_error_post(self):
        response = app.APP.test_client().post(
            "/slackroll", data=dict(text="ABS(1 - 3d30")
        )

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data,
            '{"response_type":"ephemeral","text":"Ran into a $end ($end)'
            + " where it wasn't expected, at position None.\"}\n",
        )

    def test_error_two_post(self):
        response = app.APP.test_client().post("/slackroll", data=dict(text="3d3d1d0"))

        data = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data,
            '{"response_type":"ephemeral","text":"Ran into a DICE (d0)'
            + " where it wasn't expected, at position SourcePosition(idx=5, lineno=1, colno=6).\"}\n",
        )

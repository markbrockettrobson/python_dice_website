import flask
import python_dice

import python_dice_website.interface.i_api_type as i_api_type


class SlackRollApi(i_api_type.IApi):
    _HELP_NAME = "slack roll"
    _HElP_TEXT = (
        "\n"
        "Rolls a python dice program and returns the int result or passer error\n"
        "Post request:\n"
        "   The program to be passed as json field in the body of a post request\n"
        '   eg {text: "2d6 + 2"}\n'
    )
    _ROUTE = "/slackroll"

    # pylint: disable=unused-variable, broad-except
    @staticmethod
    def add_to_app(flask_app: flask.Flask) -> None:
        @flask_app.route(SlackRollApi._ROUTE, methods=["POST"])
        def slack_roll_api():
            interpreter = python_dice.PythonDiceInterpreter()
            request_json = flask.request.get_json()
            if request_json and "text" in request_json:
                program = request_json["text"]
            else:
                payload = {"response_type": "ephemeral", "text": "no dice program!"}
                return flask.jsonify(payload)
            split_program = program.split("\n")
            try:
                return str(interpreter.roll(split_program)["stdout"])
            except Exception as exception:
                payload = {"response_type": "ephemeral", "text": f"{str(exception)}"}
                return flask.jsonify(payload)

    @staticmethod
    def get_name() -> str:
        return SlackRollApi._HELP_NAME

    @staticmethod
    def get_help_text() -> str:
        return SlackRollApi._HElP_TEXT

    @staticmethod
    def get_route() -> str:
        return SlackRollApi._ROUTE

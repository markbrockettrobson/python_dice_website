import flask
import python_dice

import python_dice_website.interface.i_api_type as i_api_type


class RollApi(i_api_type.IApi):
    _HELP_NAME = "roll"
    _HElP_TEXT = (
        "\n"
        "Rolls a python dice program and returns the int result or passer error\n"
        "Post request:\n"
        "   The program to be passed as json field in the body of a post request\n"
        '   eg {program: "2d6 + 2"}\n'
        "Get request:\n"
        "   The program to be passed as a URL parameter\n"
        "   eg roll?program=2d6%20%2B%202\n"
        '       %20 = " "\n'
        '       %2B = "+"\n'
    )
    _ROUTE = "/roll"

    # pylint: disable=unused-variable, broad-except
    @staticmethod
    def add_to_app(flask_app: flask.Flask) -> None:
        @flask_app.route(RollApi._ROUTE, methods=["POST", "GET"])
        def roll_api():
            if flask.request.method == "POST":
                return roll_api_post()
            return roll_api_get()

        def roll_api_post():
            interpreter = python_dice.PythonDiceInterpreter()
            request_json = flask.request.get_json()
            if request_json and "program" in request_json:
                program = request_json["program"]
            else:
                return f"no json program!"
            split_program = program.split("\n")
            try:
                return str(interpreter.roll(split_program)["stdout"])
            except Exception as exception:
                return f"{str(exception)}"

        def roll_api_get():
            interpreter = python_dice.PythonDiceInterpreter()
            program = flask.request.args.get("program", None)
            if program is None:
                return f"no url parameter program!"
            split_program = program.split("\n")
            try:
                return str(interpreter.roll(split_program)["stdout"])
            except Exception as exception:
                return f"{str(exception)}"

    @staticmethod
    def get_name() -> str:
        return RollApi._HELP_NAME

    @staticmethod
    def get_help_text() -> str:
        return RollApi._HElP_TEXT

    @staticmethod
    def get_route() -> str:
        return RollApi._ROUTE

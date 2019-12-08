import flask
import python_dice

import python_dice_website.interface.i_api_type as i_api_type


class RollApi(i_api_type.IApi):
    _HELP_NAME = "roll"
    _HElP_TEXT = (
        "rolls a python dice program and returns the int result or passer error"
    )
    _ROUTE = "/roll"

    # pylint: disable=unused-variable, broad-except
    @staticmethod
    def add_to_app(flask_app: flask.Flask) -> None:
        @flask_app.route(RollApi._ROUTE, methods=["POST"])
        def roll_api():
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

    @staticmethod
    def get_name() -> str:
        return RollApi._HELP_NAME

    @staticmethod
    def get_help_text() -> str:
        return RollApi._HElP_TEXT

    @staticmethod
    def get_route() -> str:
        return RollApi._ROUTE

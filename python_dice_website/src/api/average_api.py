import flask
import python_dice

import python_dice_website.interface.i_api_type as i_api_type


class AverageApi(i_api_type.IApi):
    _HELP_NAME = "Average"
    _HElP_TEXT = (
        "\n"
        "Creates a probability distribution a python dice program and returns the float result or passer error\n"
        "Post request:\n"
        "   The program to be passed as json field in the body of a post request\n"
        '   eg {program: "2d6 + 2"}\n'
        "Get request:\n"
        "   The program to be passed as a URL parameter\n"
        "   eg average?program=2d6%20%2B%202\n"
        '       %20 = " "\n'
        '       %2B = "+"\n'
    )
    _ROUTE = "/average"

    # pylint: disable=unused-variable, broad-except
    @staticmethod
    def add_to_app(flask_app: flask.Flask) -> None:
        local_logger = flask_app.logger.getChild(AverageApi.__name__)

        @flask_app.route(AverageApi._ROUTE, methods=["POST", "GET"])
        def average_api():
            local_logger.debug("request method %s", flask.request.method)
            if flask.request.method == "POST":
                return average_api_post()
            return average_api_get()

        def average_api_post():
            interpreter = python_dice.PythonDiceInterpreter()
            request_json = flask.request.get_json()
            local_logger.debug("request json %", request_json)
            if request_json and "program" in request_json:
                program = request_json["program"]
            else:
                return f"no json program!"
            split_program = program.split("\n")
            try:
                return str(interpreter.get_average(split_program)["stdout"])
            except Exception as exception:
                return f"{str(exception)}"

        def average_api_get():
            interpreter = python_dice.PythonDiceInterpreter()
            program = flask.request.args.get("program", None)
            local_logger.debug("program url arg is %s", program)
            if program is None:
                return f"no url parameter program!"
            split_program = program.split("\n")
            try:
                return str(interpreter.get_average(split_program)["stdout"])
            except Exception as exception:
                return f"{str(exception)}"

    @staticmethod
    def get_name() -> str:
        return AverageApi._HELP_NAME

    @staticmethod
    def get_help_text() -> str:
        return AverageApi._HElP_TEXT

    @staticmethod
    def get_route() -> str:
        return AverageApi._ROUTE

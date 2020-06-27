import io
import typing

import flask
import python_dice

import python_dice_website.interface.i_api_type as i_api_type


class HistogramApi(i_api_type.IApi):
    _HELP_NAME = "Histogram"
    _HElP_TEXT = (
        "\n"
        "Creates a probability distribution a python dice program and returns the image result or passer error\n"
        "Post request:\n"
        "   The program to be passed as json field in the body of a post request\n"
        '   eg {program: "2d6 + 2"}\n'
        "Get request:\n"
        "   The program to be passed as a URL parameter\n"
        "   eg histogram?program=2d6%20%2B%202\n"
        '       %20 = " "\n'
        '       %2B = "+"\n'
    )
    _ROUTE = "/histogram"

    # pylint: disable=unused-variable, broad-except
    @staticmethod
    def add_to_app(flask_app: flask.Flask) -> None:
        local_logger = flask_app.logger.getChild(HistogramApi.__name__)

        @flask_app.route(HistogramApi._ROUTE, methods=["POST", "GET"])
        def histogram_api():
            local_logger.debug("request method %s", flask.request.method)
            if flask.request.method == "POST":
                return histogram_api_post()
            return histogram_api_get()

        def histogram_api_post():
            request_json = flask.request.get_json()
            local_logger.debug("request json %", request_json)
            if request_json and "program" in request_json:
                program = request_json["program"]
            else:
                return f"no json program!"
            split_program = program.split("\n")
            return get_image_send_file(split_program)

        def histogram_api_get():
            program = flask.request.args.get("program", None)
            if program is None:
                return f"no url parameter program!"
            split_program = program.split("\n")
            return get_image_send_file(split_program)

        def get_image_send_file(split_program: typing.List[str]):
            interpreter = python_dice.PythonDiceInterpreter()
            try:
                image = interpreter.get_histogram(split_program)
                file_pointer = io.BytesIO()
                image.save(file_pointer, format="png")
                file_pointer.seek(0)
                return flask.send_file(
                    file_pointer,
                    attachment_filename="histogram.png",
                    as_attachment=False,
                    add_etags=False,
                )
            except Exception as exception:
                return f"{str(exception)}"

    @staticmethod
    def get_name() -> str:
        return HistogramApi._HELP_NAME

    @staticmethod
    def get_help_text() -> str:
        return HistogramApi._HElP_TEXT

    @staticmethod
    def get_route() -> str:
        return HistogramApi._ROUTE

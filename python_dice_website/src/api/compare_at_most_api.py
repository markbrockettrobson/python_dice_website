import io
import typing

import flask
import python_dice

import python_dice_website.interface.i_api_type as i_api_type


class CompareAtMostApi(i_api_type.IApi):
    _HELP_NAME = "compare at least"
    _HElP_TEXT = (
        "\n"
        "Creates a probability distribution of two python dice program and returns the image result or passer error\n"
        "Post request:\n"
        "   The program to be passed as json field in the body of a post request\n"
        '   eg {program_one: "2d6 + 2", program_two: "2d10 - 2"}\n'
        "Get request:\n"
        "   The program to be passed as a URL parameter\n"
        "   eg compareatmost?program_one=2d6%20%2B%202&program_two=2d10%20-%202\n"
        '       %20 = " "\n'
        '       %2B = "+"\n'
    )
    _ROUTE = "/compareatmost"

    # pylint: disable=unused-variable, broad-except
    @staticmethod
    def add_to_app(flask_app: flask.Flask) -> None:
        @flask_app.route(CompareAtMostApi._ROUTE, methods=["POST", "GET"])
        def compare_at_most_api():
            if flask.request.method == "POST":
                return compare_at_most_api_post()
            return compare_at_most_api_get()

        def compare_at_most_api_post():
            request_json = flask.request.get_json()
            if (
                request_json
                and "program_one" in request_json
                and "program_two" in request_json
            ):
                program_one = request_json["program_one"]
                program_two = request_json["program_two"]
            else:
                return f"no json program_one and/or program_two!"

            name_one = "Program one"
            name_two = "Program two"
            if "program_one_name" in request_json:
                name_one = request_json["program_one_name"]
            if "program_one_name" in request_json:
                name_two = request_json["program_two_name"]

            split_program_one = program_one.split("\n")
            split_program_two = program_two.split("\n")
            return get_image_send_file(
                split_program_one, split_program_two, name_one, name_two
            )

        def compare_at_most_api_get():
            program_one = flask.request.args.get("program_one", None)
            if program_one is None:
                return f"no url parameter program_one!"
            program_two = flask.request.args.get("program_two", None)
            if program_two is None:
                return f"no url parameter program_two!"

            name_one = flask.request.args.get("program_one_name", None)
            name_two = flask.request.args.get("program_two_name", None)
            if name_one is None:
                name_one = "Program one"
            if name_two is None:
                name_two = "Program two"

            split_program_one = program_one.split("\n")
            split_program_two = program_two.split("\n")
            return get_image_send_file(
                split_program_one, split_program_two, name_one, name_two
            )

        def get_image_send_file(
            split_program_one: typing.List[str],
            split_program_two: typing.List[str],
            name_one: str = "Program one",
            name_two: str = "Program two",
        ):
            interpreter = python_dice.PythonDiceInterpreter()
            try:
                program_one_distribution = interpreter.get_probability_distributions(
                    split_program_one
                )["stdout"]
                program_two_distribution = interpreter.get_probability_distributions(
                    split_program_two
                )["stdout"]
                image = program_one_distribution.get_compare_at_most_histogram(
                    program_two_distribution, name_one, name_two
                )
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
        return CompareAtMostApi._HELP_NAME

    @staticmethod
    def get_help_text() -> str:
        return CompareAtMostApi._HElP_TEXT

    @staticmethod
    def get_route() -> str:
        return CompareAtMostApi._ROUTE

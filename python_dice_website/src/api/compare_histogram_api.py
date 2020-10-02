import flask
import flask_restplus.api as api
import flask_restplus.fields as fields
import flask_restplus.resource as resource

import python_dice_website.interface.i_api_type as i_api_type
import python_dice_website.interface.i_pil_image_sender as i_pil_image_sender
import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory
import python_dice_website.src.global_logger as global_logger


class CompareHistogramApi(i_api_type.IApi):
    _ROUTE = "/compare_histogram"

    def __init__(
        self,
        python_dice_interpreter_factory: i_python_dice_interpreter_factory.IPythonDiceInterpreterFactory,
        pil_image_sender: i_pil_image_sender.IPilImageSender,
    ):
        self._pil_image_sender = pil_image_sender
        self._python_dice_interpreter_factory = python_dice_interpreter_factory

    # pylint: disable=unused-variable, broad-except
    def add_to_app(self, flask_api: api.Api, name_space: api.Namespace) -> None:
        local_logger = global_logger.ROOT_LOGGER.getChild(CompareHistogramApi.__name__)

        flask_resource_fields = flask_api.model(
            "compare histogram programs",
            {
                "program_one": fields.String(
                    required=True,
                    description="The 1st Python Dice program to run",
                    example="2d20k1",
                ),
                "program_two": fields.String(
                    required=True,
                    description="The 2nd Python Dice program to run",
                    example="2d20d1",
                ),
            },
        )

        flask_resource_parser = flask_api.parser()
        flask_resource_parser.add_argument(
            "program_one",
            type=str,
            help="The 1st Python Dice program to run",
            location="args",
            required=True,
            ignore=False,
            nullable=False,
        )
        flask_resource_parser.add_argument(
            "program_two",
            type=str,
            help="The 2nd Python Dice program to run",
            location="args",
            required=True,
            ignore=False,
            nullable=False,
        )
        pil_image_sender = self._pil_image_sender
        python_dice_interpreter_factory = self._python_dice_interpreter_factory

        # pylint: disable=unused-variable, broad-except
        @name_space.route(self.route)
        class CompareHistogram(resource.Resource):
            @staticmethod
            @flask_api.expect(flask_resource_fields)
            def post():
                request_json = flask.request.get_json()
                local_logger.debug("request json %s", request_json)
                if (
                    request_json
                    and "program_one" in request_json
                    and "program_two" in request_json
                ):
                    program_one = request_json["program_one"]
                    program_two = request_json["program_two"]
                else:
                    return f"No json program_one and/or program_two.", 400

                split_program_one = program_one.split("\n")
                split_program_two = program_two.split("\n")
                interpreter = python_dice_interpreter_factory.get_interpreter()

                try:
                    program_one_distribution = interpreter.get_probability_distributions(
                        split_program_one
                    )[
                        "stdout"
                    ]
                    program_two_distribution = interpreter.get_probability_distributions(
                        split_program_two
                    )[
                        "stdout"
                    ]
                    image = program_one_distribution.get_compare_histogram(
                        program_two_distribution
                    )
                    return pil_image_sender.send_image(pil_image=image)
                except Exception as exception:
                    return f"{str(exception)}", 400

            @staticmethod
            @flask_api.expect(flask_resource_parser)
            def get():
                program_one = flask.request.args.get("program_one", None)
                local_logger.debug("program one url arg is %s", program_one)
                if program_one is None:
                    return f"No url parameter program_one.", 400
                program_two = flask.request.args.get("program_two", None)
                local_logger.debug("program two url arg is %s", program_two)
                if program_two is None:
                    return f"No url parameter program_two.", 400

                split_program_one = program_one.split("\n")
                split_program_two = program_two.split("\n")
                interpreter = python_dice_interpreter_factory.get_interpreter()

                try:
                    program_one_distribution = interpreter.get_probability_distributions(
                        split_program_one
                    )[
                        "stdout"
                    ]
                    program_two_distribution = interpreter.get_probability_distributions(
                        split_program_two
                    )[
                        "stdout"
                    ]
                    image = program_one_distribution.get_compare_histogram(
                        program_two_distribution
                    )
                    return pil_image_sender.send_image(pil_image=image)
                except Exception as exception:
                    return f"{str(exception)}", 400

    @property
    def route(self) -> str:
        return self._ROUTE

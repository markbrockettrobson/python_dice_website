import flask
import flask_restplus.api as api
import flask_restplus.fields as fields
import flask_restplus.resource as resource

import python_dice_website.interface.i_api_type as i_api_type
import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory
import python_dice_website.interface.i_usage_limiter as i_usage_limiter
import python_dice_website.src.global_logger as global_logger


class AverageApi(i_api_type.IApi):
    _ROUTE = "/average"

    def __init__(
        self,
        python_dice_interpreter_factory: i_python_dice_interpreter_factory.IPythonDiceInterpreterFactory,
        usage_limiter: i_usage_limiter.IUsageLimiter,
    ):
        self._python_dice_interpreter_factory = python_dice_interpreter_factory
        self._usage_limiter = usage_limiter

    # pylint: disable=unused-variable, broad-except
    def add_to_app(self, flask_api: api.Api, name_space: api.Namespace) -> None:
        local_logger = global_logger.ROOT_LOGGER.getChild(AverageApi.__name__)

        flask_resource_fields = flask_api.model(
            "program",
            {
                "program": fields.String(
                    required=True,
                    description="The Python Dice program to run",
                    example="2d20k1",
                )
            },
        )

        flask_resource_parser = flask_api.parser()
        flask_resource_parser.add_argument(
            "program",
            type=str,
            help="The Python Dice program to run",
            location="args",
            required=True,
            ignore=False,
            nullable=False,
        )

        python_dice_interpreter_factory = self._python_dice_interpreter_factory
        usage_limiter = self._usage_limiter

        # pylint: disable=unused-variable, broad-except
        @name_space.route(self.route)
        class Average(resource.Resource):
            @staticmethod
            @flask_api.expect(flask_resource_fields)
            def post():
                interpreter = python_dice_interpreter_factory.get_interpreter()
                request_json = flask.request.get_json()
                local_logger.debug("request json %s", request_json)
                if request_json and "program" in request_json:
                    program = request_json["program"]
                else:
                    return f"No program in request json.", 400
                split_program = program.split("\n")
                try:
                    if usage_limiter.is_over_limit(split_program):
                        return usage_limiter.get_over_limit_message(), 400
                    return interpreter.get_average(split_program)["stdout"]
                except Exception as exception:
                    return f"{str(exception)}", 400

            @staticmethod
            @flask_api.expect(flask_resource_parser)
            def get():
                interpreter = python_dice_interpreter_factory.get_interpreter()
                program = flask.request.args.get("program", None)
                local_logger.debug("program url arg is %s", program)
                if program is None:
                    return f"No url parameter program.", 400
                split_program = program.split("\n")
                try:
                    if usage_limiter.is_over_limit(split_program):
                        return usage_limiter.get_over_limit_message(), 400
                    return interpreter.get_average(split_program)["stdout"]
                except Exception as exception:
                    return f"{str(exception)}", 400

    @property
    def route(self) -> str:
        return self._ROUTE

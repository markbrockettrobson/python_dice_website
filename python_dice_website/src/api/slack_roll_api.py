import flask
import flask_restplus.api as api
import flask_restplus.resource as resource

import python_dice_website.interface.i_api_type as i_api_type
import python_dice_website.interface.i_python_dice_interpreter_factory as i_python_dice_interpreter_factory
import python_dice_website.interface.i_usage_limiter as i_usage_limiter
import python_dice_website.src.global_logger as global_logger


class SlackRollApi(i_api_type.IApi):
    _ROUTE = "/slack_roll"

    def __init__(
        self,
        python_dice_interpreter_factory: i_python_dice_interpreter_factory.IPythonDiceInterpreterFactory,
        usage_limiter: i_usage_limiter.IUsageLimiter,
    ):
        self._python_dice_interpreter_factory = python_dice_interpreter_factory
        self._usage_limiter = usage_limiter

    # pylint: disable=unused-variable, broad-except
    def add_to_app(self, flask_api: api.Api, name_space: api.Namespace) -> None:
        local_logger = global_logger.ROOT_LOGGER.getChild(SlackRollApi.__name__)

        flask_resource_parser = flask_api.parser()
        flask_resource_parser.add_argument(
            "text",
            type=str,
            help="The slack message text field, for example /roll 1d20 , "
            "text would be 1d20. for details on setting the slack side see "
            "https://api.slack.com/interactivity/slash-commands",
            location="form",
            required=True,
            ignore=False,
            nullable=False,
        )
        python_dice_interpreter_factory = self._python_dice_interpreter_factory
        usage_limiter = self._usage_limiter

        # pylint: disable=unused-variable, broad-except
        @name_space.route(self.route)
        class SlackRoll(resource.Resource):
            @staticmethod
            @flask_api.expect(flask_resource_parser)
            def post():
                local_logger.debug("request method %s", flask.request.method)
                interpreter = python_dice_interpreter_factory.get_interpreter()
                program = flask.request.form.get("text", None)

                local_logger.debug("request text is %s", program)
                if program is None:
                    payload = {"response_type": "ephemeral", "text": "no dice program!"}
                    local_logger.debug("return %s", payload)
                    return flask.jsonify(payload)
                split_program = program.split("\n")
                try:
                    if usage_limiter.is_over_limit(split_program):
                        return usage_limiter.get_over_limit_message(), 400
                    payload = {
                        "response_type": "in_channel",
                        "blocks": [
                            {
                                "type": "section",
                                "text": {"type": "mrkdwn", "text": program},
                            },
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": str(
                                        interpreter.roll(split_program)["stdout"]
                                    ),
                                },
                            },
                        ],
                    }
                    local_logger.debug("return %s", payload)
                    return flask.jsonify(payload)
                except Exception as exception:
                    payload = {
                        "response_type": "ephemeral",
                        "text": f"{str(exception)}",
                    }
                    local_logger.debug("return %s", payload)
                    return flask.jsonify(payload)

    @property
    def route(self) -> str:
        return self._ROUTE

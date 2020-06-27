import flask

import python_dice_website.interface.i_api_type as i_api_type


class PrivacyApi(i_api_type.IApi):
    _HELP_NAME = "privacy"
    _HElP_TEXT = "returns the privacy policy of the app"
    _ROUTE = "/privacy"

    # pylint: disable=unused-variable, broad-except
    @staticmethod
    def add_to_app(flask_app: flask.Flask) -> None:
        local_logger = flask_app.logger.getChild(PrivacyApi.__name__)

        @flask_app.route(PrivacyApi._ROUTE, methods=["GET"])
        def privacy_api():
            return flask.render_template("PrivacyPolicy.html")

    @staticmethod
    def get_name() -> str:
        return PrivacyApi._HELP_NAME

    @staticmethod
    def get_help_text() -> str:
        return PrivacyApi._HElP_TEXT

    @staticmethod
    def get_route() -> str:
        return PrivacyApi._ROUTE

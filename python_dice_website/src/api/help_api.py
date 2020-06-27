import flask

import python_dice_website.interface.i_api_type as i_api_type
import python_dice_website.src.api.api_list as api_list


class HelpApi(i_api_type.IApi):
    _HELP_NAME = "Help page"
    _HElP_TEXT = "index of the API"
    _ROUTE = "/"

    # pylint: disable=unused-variable
    @staticmethod
    def add_to_app(flask_app: flask.Flask) -> None:
        local_logger = flask_app.logger.getChild(HelpApi.__name__)

        @flask_app.route(HelpApi._ROUTE)
        def help_api():
            help_table = {
                api.get_name(): (api.get_help_text(), api.get_route())
                for api in api_list.API_LIST
            }
            help_table[HelpApi._HELP_NAME] = (HelpApi._HElP_TEXT, HelpApi._ROUTE)
            return flask.render_template("help_api.html", help_table=help_table)

    @staticmethod
    def get_name() -> str:
        return HelpApi._HELP_NAME

    @staticmethod
    def get_help_text() -> str:
        return HelpApi._HElP_TEXT

    @staticmethod
    def get_route() -> str:
        return HelpApi._ROUTE

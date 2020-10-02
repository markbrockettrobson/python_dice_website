import flask
import flask_restplus.api as api
import flask_restplus.resource as resource

import python_dice_website.interface.i_api_type as i_api_type
import python_dice_website.src.global_logger as global_logger


class PrivacyApi(i_api_type.IApi):
    _ROUTE = "/privacy"

    # pylint: disable=unused-variable, broad-except
    def add_to_app(self, flask_api: api.Api, name_space: api.Namespace) -> None:
        local_logger = global_logger.ROOT_LOGGER.getChild(PrivacyApi.__name__)

        # pylint: disable=unused-variable, broad-except
        @name_space.route(self.route)
        class Privacy(resource.Resource):
            @staticmethod
            def get():
                local_logger.warning("someone looked at PrivacyPolicy")
                return flask.render_template("PrivacyPolicy.html")

    @property
    def route(self) -> str:
        return self._ROUTE

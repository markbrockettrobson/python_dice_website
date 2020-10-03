import os
import typing

import flask
import flask_restplus

import python_dice_website.interface.i_api_type as i_api_type
import python_dice_website.src.global_logger as global_logger


class PythonDiceWebApp:
    def __init__(
        self,
        api_list: typing.List[i_api_type.IApi],
        host: str = "0.0.0.0",
        debug: bool = False,
        port: int = int(os.environ.get("PORT", 8080)),
        logging: bool = True,
        https_server: bool = False,
    ):
        self._app = flask.Flask(__name__)
        self._api = flask_restplus.Api(
            self._app,
            version="1.0",
            title="Python Dice Rest Api",
            description="""
        a simple Rest API for Python Dice. 
        for syntax descriptions of python dice see https://github.com/markbrockettrobson/python_dice
        Please let me know if anything is not working. https://github.com/markbrockettrobson/python_dice_website
        If you need any help running this website feel free to ask
        """,
        )
        self._name_space = self._api.namespace(
            "api", description="simple Rest API for Python Dice"
        )
        self._debug = debug
        self._host = host
        self._port = port

        logger = None
        if logging:
            logger = global_logger.ROOT_LOGGER.getChild(PythonDiceWebApp.__name__)

        for api in api_list:
            if logger:
                logger.info("adding api %s to app.", api.route)
            api.add_to_app(self._api, self._name_space)

        if https_server:
            self._api.specs_url = flask.url_for("", _external=True, _scheme="https")

    def get_app(self) -> flask.Flask:
        return self._app

    def run(self) -> None:
        self._app.run(host=self._host, debug=self._debug, port=self._port)

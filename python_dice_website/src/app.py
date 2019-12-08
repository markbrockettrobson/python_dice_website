import os

import flask

import python_dice_website.src.api.api_list as api_list
import python_dice_website.src.api.help_api as help_api


class PythonDiceWebApp:
    def __init__(
        self,
        host: str = "0.0.0.0",
        debug: bool = False,
        port: int = int(os.environ.get("PORT", 8080)),
    ):
        self._app = flask.Flask(__name__)
        self._debug = debug
        self._host = host
        self._port = port

        help_api.HelpApi.add_to_app(self._app)
        for api in api_list.API_LIST:
            api.add_to_app(self._app)

    def get_app(self) -> flask.Flask:
        return self._app

    def run(self) -> None:
        self._app.run(host=self._host, debug=self._debug, port=self._port)


APP = PythonDiceWebApp().get_app()

if __name__ == "__main__":
    PythonDiceWebApp(host="localhost", debug=True, port=5000).run()

import os

import flask


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

        # pylint: disable=unused-variable
        @self._app.route("/")
        def hello_world():
            return "Hello World"

    def get_app(self) -> flask.Flask:
        return self._app

    def run(self) -> None:
        self._app.run(host=self._host, debug=self._debug, port=self._port)


APP = PythonDiceWebApp().get_app()

if __name__ == "__main__":
    PythonDiceWebApp().run()

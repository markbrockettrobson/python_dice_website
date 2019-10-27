import os

import flask


def app(_, __):
    PythonDiceWebApp().run()


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

    def run(self):
        self._app.run(host=self._host, debug=self._debug, port=self._port)


if __name__ == "__main__":
    PythonDiceWebApp(
        host="localhost", debug=True, port=int(os.environ.get("PORT", 8080))
    ).run()

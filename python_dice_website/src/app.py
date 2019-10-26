import flask


class PythonDiceWebApp:
    def __init__(self, host: str = "localhost", debug: bool = False, port=5000):
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
    PythonDiceWebApp(host="0.0.0.0", debug=True, port=5000).run()

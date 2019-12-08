import abc

import flask


class IApi(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def add_to_app(flask_app: flask.Flask) -> None:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_name() -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_help_text() -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def get_route() -> str:
        pass

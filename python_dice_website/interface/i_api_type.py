import abc

import flask_restplus.api as api


class IApi(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def add_to_app(flask_api: api.Api, name_space: api.Namespace) -> None:
        pass

    @property
    @abc.abstractmethod
    def route(self) -> str:
        pass

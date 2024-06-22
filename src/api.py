from abc import ABC, abstractmethod
from json import JSONDecodeError

from requests import Response
import requests
from urllib3.util import url

from config import HH_URL
from src.exceptions import HhAPIException


class API(ABC):
    """
    Абстрактный класс для подключения и получения данных с API ресурса
    """

    @property
    @abstractmethod
    def url(self) -> str:
        """
        Свойство для получения базового URL для обращения к API
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def get_response_data(self) -> list[dict]:
        """

        :return:
        """
        raise NotImplementedError()


    @abstractmethod
    def _get_response(self) -> Response:
        """

        :return:
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def _check_status(response: Response) -> bool:
        """

        :return:
        """
        raise NotImplementedError()


class HhAPI(API):

    def __init__(self) -> None:
        self.__text = None
        self.__params = {
            "per_page": 100,
            "search_field": "name",
        }

    @property
    def url(self) -> str:
        return HH_URL

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, text:str) -> None:
        self.__text = text

    def _get_response(self) -> Response:
        if self.__text is None:
            raise HhAPIException("Поисковый запрос не задан")
        self.__params["text"] = self.__text
        return requests.get(HH_URL, params=self.__params)

    def get_response_data(self) -> list[dict]:
        response = self._get_response()
        is_allowed = self._check_status(response)
        if not is_allowed:
            raise HhAPIException(f"Ошибка запроса данных status_code: {response:status_code}, response:{response:text}")
        try:
            return response.json()
        except JSONDecodeError:
            raise HhAPIException(f"Ошибка получения данных, получен не json объект response:{response:text}")


    @staticmethod
    def _check_status(response: Response) -> bool:
        return response.status_code == 200


if __name__ == '__main__':
    hh = HhAPI()
    hh.text = "python"

    data = hh.get_response_data()

    print(data)
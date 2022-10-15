"""Задачи для работы с сетью.

Обработка ссылок (GET-запросы) и анализ полученного результата.
"""
from datetime import date
from operator import attrgetter

import requests
from pydantic import BaseModel

from job import Job
from settings import settings


class CelebrateResponse(BaseModel):
    title: str


class Response(BaseModel):
    date: date
    celebrations: list[CelebrateResponse]


class ChurchCalendar(Job):
    """Церковный календарь.

    Подскажет названия праздников по дате.
    """

    def __init__(
        self,
        *,
        dates: list[date] | None = None,
        lang: str = settings.default_lang,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.dates = dates or []
        self.lang = lang

    def run(self):
        for date_ in self.dates:
            url = self._get_url(date_)
            response = self._get_response(url)
            yield self._format_response(response)

    def _get_url(self, date_: date):
        return (
            f'http://calapi.inadiutorium.cz/api/v0/'
            f'{self.lang}/calendars/default/'
            f'{date_.year}/{date_.month}/{date_.day}'
        )

    def _get_response(self, url) -> Response:
        response = requests.get(url)
        json_response = response.json()
        return Response(**json_response)

    def _format_response(self, response: Response) -> str:
        if celebrations := response.celebrations:
            headers = map(attrgetter('title'), celebrations)
            concat_headers = ' and '.join(headers)
            return f'Today ({response.date}) is {concat_headers}.'

        return f'There are no celebrations today ({response.date}).'

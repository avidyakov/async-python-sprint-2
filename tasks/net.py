"""Задачи для работы с сетью.

Обработка ссылок (GET-запросы) и анализ полученного результата.
"""
from datetime import date
from operator import attrgetter
from typing import Iterator

import requests
from pydantic import BaseModel

from settings import settings


class CelebrateResponse(BaseModel):
    title: str


class Response(BaseModel):
    date: date
    celebrations: list[CelebrateResponse]


def church_calendar(dates: list[date]) -> Iterator[str]:
    for date_ in dates:
        url = _get_url(date_)
        response = _get_response(url)
        yield _format_response(response)


def _get_url(date_: date) -> str:
    return (
        f'http://calapi.inadiutorium.cz/api/v0/'
        f'{settings.default_lang}/calendars/default/'
        f'{date_.year}/{date_.month}/{date_.day}'
    )


def _get_response(url: str) -> Response:
    response = requests.get(url)
    json_response = response.json()
    return Response(**json_response)


def _format_response(response: Response) -> str:
    if celebrations := response.celebrations:
        headers = map(attrgetter('title'), celebrations)
        concat_headers = ' and '.join(headers)
        return f'Today ({response.date}) is {concat_headers}.'

    return f'There are no celebrations today ({response.date}).'

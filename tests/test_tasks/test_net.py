from datetime import date

import pytest

from tasks.net import ChurchCalendar, Response


class TestChurchCalendar:
    @pytest.fixture
    def calendar(self) -> ChurchCalendar:
        return ChurchCalendar()

    def test_run(self):
        calendar = ChurchCalendar(
            dates=[date(2022, 12, 25)],
        )

        for holiday in calendar.run():
            assert holiday == 'Today (2022-12-25) is Christmas.'

    def test_get_url(self, calendar, data_provider):
        test_date = date(2015, 6, 27)
        url = calendar._get_url(test_date)

        expected = (
            'http://calapi.inadiutorium.cz/api/v0/'
            'en/calendars/default/2015/6/27'
        )
        assert url == expected

    def test_get_response(self, calendar):
        url = (
            'http://calapi.inadiutorium.cz/'
            'api/v0/en/calendars/default/2022/12/25'
        )
        response = calendar._get_response(url)

        expected = Response(
            date='2022-12-25', celebrations=[{'title': 'Christmas'}]
        )
        assert response == expected

    @pytest.mark.parametrize(
        'date_, celebrations, expected',
        [
            (
                '2022-12-25',
                [{'title': 'Christmas'}],
                'Today (2022-12-25) is Christmas.',
            ),
            (
                '2022-12-25',
                [{'title': 'Christmas'}, {'title': 'New Year'}],
                'Today (2022-12-25) is Christmas and New Year.',
            ),
            (
                '2022-12-25',
                [],
                'There are no celebrations today (2022-12-25).',
            ),
        ],
    )
    def test_format_response(self, calendar, date_, celebrations, expected):
        response = Response(date=date_, celebrations=celebrations)

        formatted = calendar._format_response(response)

        assert formatted == expected

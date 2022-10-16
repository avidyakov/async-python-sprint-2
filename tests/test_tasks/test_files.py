from pathlib import Path

import pytest

from settings import settings
from tasks.errors import BadPathError
from tasks.files import CalendarStorage


class TestCalendarStorage:
    @pytest.fixture
    def storage(self):
        return CalendarStorage()

    def test_run(self, storage, data_provider):
        date = data_provider.datetime.date()
        text = data_provider.text.text()

        gen = storage.run()
        gen.send(None)
        gen.send(date)
        gen.send(text)
        gen.close()

        file_path = storage.target_dir / date.strftime('%Y-%m-%d.txt')
        assert file_path.exists()
        assert file_path.read_text() == text

    def test_set_target_dir(self, storage):
        storage.target_dir = settings.default_dir

        assert storage._target_dir == settings.default_dir.resolve()

    @pytest.mark.parametrize(
        'path', [Path('../../README.md'), Path('./i_dont_exist')]
    )
    def test_set_bad_target_dir(self, storage, path):
        with pytest.raises(BadPathError):
            storage.target_dir = path

    def test_get_target_dir(self, storage):
        storage.target_dir = settings.default_dir

        assert storage.target_dir == settings.default_dir.resolve()

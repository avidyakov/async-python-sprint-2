"""Задачи для работы с файлами.

Создание, чтение, запись.
"""

from pathlib import Path

from job import Job
from settings import settings
from tasks.errors import BadPathError


class CalendarStorage(Job):
    def __init__(self, *, target_dir: Path = settings.default_dir, **kwargs):
        self.target_dir = target_dir

        super().__init__(**kwargs)

    @property
    def target_dir(self):
        return self._target_dir

    @target_dir.setter
    def target_dir(self, path: Path):
        path = path.resolve()
        if not path.is_dir():
            raise BadPathError(path)

        self._target_dir = path

    def run(self):
        while date := (yield):
            file_path = self.target_dir / date.strftime('%Y-%m-%d.txt')
            text = yield
            file_path.write_text(text)

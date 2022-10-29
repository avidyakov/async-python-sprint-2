from datetime import datetime
from typing import Any, Generator, Iterator

import backoff
from loguru import logger


class Job:
    def __init__(
        self,
        gen: Generator,
        *,
        start_at: datetime | None = None,
        max_working_time: int | None = None,
        tries: int | None = None,
        dependencies: list['Job'] = None,
    ):
        self._gen = gen
        self._start_at = start_at
        self._max_working_time = max_working_time
        self._tries = tries
        self._dependencies = dependencies or []
        self._start_time = None

    def run(self) -> Iterator[Any]:
        while self._dependencies:
            yield from self._run_dependencies()

        if self._start_at and datetime.now() < self._start_at:
            yield

        if self._start_time is None:
            self._start_time = datetime.now()
            logger.info(f'Job {self} started at {self._start_time}')

        yield from self._run()

    def _run_dependencies(self) -> Iterator[Any]:
        for job in self._dependencies:
            try:
                yield next(job.run())
            except StopIteration:
                self._dependencies.remove(job)

    def _run(self) -> Iterator[Any]:
        @backoff.on_exception(
            backoff.expo,
            Exception,
            max_tries=self._tries,
        )
        def inner():
            while True:
                if self._has_expired():
                    break

                try:
                    yield next(self._gen)
                except StopIteration:
                    break

        return inner()

    def _has_expired(self) -> bool:
        return (
            self._max_working_time
            and datetime.now() - self._start_time > self._max_working_time
        )

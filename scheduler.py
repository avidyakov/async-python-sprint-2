from typing import NoReturn

from loguru import logger

from errors import PoolSizeError
from job import Job
from settings import settings


class Scheduler:
    def __init__(self, pool_size: int = settings.default_pool_size):
        self._pool_size = pool_size
        self._jobs: list[Job] = []

    def schedule(self, job: Job) -> NoReturn:
        if len(self._jobs) >= self._pool_size:
            logger.error(f'Pool size exceeded: {self._pool_size}')
            raise PoolSizeError(f'Maximum pool size {len(self._jobs)} tasks')

        self._jobs.append(job)

    def run(self) -> NoReturn:
        while self._jobs:
            self._run_jobs()

    def _run_jobs(self) -> NoReturn:
        for job in self._jobs:
            self._run_job(job)

    def _run_job(self, job: Job) -> NoReturn:
        try:
            result = next(job.run())
            logger.info(f'Job {job} result: {result}')
        except StopIteration:
            self._jobs.remove(job)
            logger.info(f'Job {job} finished')

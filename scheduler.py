from datetime import datetime

from exceptions import PoolSizeError
from job import Job
from settings import settings


class Scheduler:
    def __init__(self, pool_size: int = settings.default_pool_size):
        self._pool_size = pool_size
        self._jobs: list[Job] = []

    def schedule(self, job: Job):
        if len(self._jobs) >= self._pool_size:
            raise PoolSizeError(f'Maximum pool size {len(self._jobs)} tasks')

        self._jobs.append(job)

    def run(self):
        while self._jobs:
            self._run_jobs()

    def _run_jobs(self):
        for job in self._jobs:
            self._run_job(job)

    def _run_job(self, job):
        if job.start_at is None or datetime.now() >= job.start_at:
            job.set_start_time()

        if job.get_start_time():
            try:
                next(job.get_gen())
            except StopIteration:
                self._jobs.remove(job)

from job import Job
from settings import settings


class Scheduler:
    def __init__(self, pool_size: int = settings.default_pool_size):
        self._pool_size = pool_size
        self._jobs: list[Job] = []

    def schedule(self, job: Job):
        self._jobs.append(job)

    def run(self):
        pass

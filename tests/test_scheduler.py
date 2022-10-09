from job import Job
from scheduler import Scheduler


class TestScheduler:
    def test_schedule(self):
        scheduler = Scheduler()
        job = Job()

        scheduler.schedule(job)

        assert scheduler._jobs == [job]

"""В README.md указана инструкция по запуску проекта"""

from datetime import date
from typing import NoReturn

from job import Job
from scheduler import Scheduler
from tasks.net import church_calendar

DATES = [
    date(2021, 1, 1),
    date(2021, 1, 2),
    date(2021, 12, 25),
]


def main() -> NoReturn:
    gen = church_calendar(DATES)
    job1 = Job(gen)
    scheduler = Scheduler()
    scheduler.schedule(job1)
    scheduler.run()


if __name__ == '__main__':
    main()

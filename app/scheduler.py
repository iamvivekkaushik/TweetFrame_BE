from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from sqlalchemy.orm import Session

from app.config import DATABASE_URL

# AP Scheduler config
from app.database.core import get_db
from app.schedule.job_handler import handle_schedule
from app.schedule.repository import ScheduleRepository

JOB_STORE = {"default": SQLAlchemyJobStore(url=DATABASE_URL.__str__())}
EXECUTORS = {
    "default": ThreadPoolExecutor(20),
}
JOB_DEFAULT = {"coalesce": False, "max_instances": 3}

scheduler = BackgroundScheduler(
    executors=EXECUTORS, job_defaults=JOB_DEFAULT, timezone=utc
)


def init_scheduler():
    scheduler.start()

    db: Session = next(get_db())
    schedule_repo = ScheduleRepository(db)

    schedule_list = schedule_repo.all_active_schedules()

    for schedule in schedule_list:
        scheduler.add_job(
            func=handle_schedule,
            kwargs={"schedule_id": schedule.id},
            max_instances=1,
            id=str(schedule.id),
            replace_existing=True,
        )

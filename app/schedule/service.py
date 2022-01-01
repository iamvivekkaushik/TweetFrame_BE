from app.enums import ScheduleStatus
from app.schedule.models import ScheduleUpdate, Schedule
from app.schedule.repository import ScheduleRepository


def update_schedule_status(
    schedule_repo: ScheduleRepository,
    schedule: Schedule,
    status: ScheduleStatus,
    message: str = "",
) -> Schedule:
    schedule_update: ScheduleUpdate = ScheduleUpdate(
        status=status.value, message=message
    )
    schedule: Schedule = schedule_repo.update(
        object_id=schedule.id, obj_in=schedule_update
    )
    return schedule

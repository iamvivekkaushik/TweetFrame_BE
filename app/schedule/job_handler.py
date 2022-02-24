from sqlalchemy.orm import Session

from app.database.core import get_db
from app.enums import ScheduleStatus
from app.purchase.models import Purchase, PurchaseUpdate
from app.purchase.repository import PurchaseRepository
from app.schedule.models import Schedule
from app.schedule.repository import ScheduleRepository
from app.schedule.service import update_schedule_status
from app.twitter.service import update_profile_image
from app.user.models import User, UserUpdate
from app.user.repository import UserRepository


def handle_schedule(**kwargs):
    schedule_id = kwargs["schedule_id"]

    # Get all the New, Unfinished or running jobs
    db: Session = next(get_db())
    schedule_repo = ScheduleRepository(db)
    schedule: Schedule = schedule_repo.get(schedule_id)
    user: User = schedule.created_by

    if not schedule:
        update_schedule_status(
            schedule_repo,
            schedule,
            ScheduleStatus.FAILED,
            message="Schedule not found",
        )
        return

    try:
        # Update Schedule Status
        update_schedule_status(schedule_repo, schedule, ScheduleStatus.IN_PROGRESS)

        # purchase_repo = PurchaseRepository(db)
        # purchase: Purchase = purchase_repo.get_active_purchase(user)
        #
        # if not purchase or purchase.is_active is False:
        #     # Update Schedule Status
        #     update_schedule_status(
        #         schedule_repo,
        #         schedule,
        #         ScheduleStatus.FAILED,
        #         message="No active purchase found",
        #     )
        #     return

        # remaining_frames = purchase.remaining_frame_usage

        # if remaining_frames <= 0:
        # Update Schedule Status
        # update_schedule_status(
        #     schedule_repo,
        #     schedule,
        #     ScheduleStatus.FAILED,
        #     message="No remaining frames.",
        # )
        # return

        frame = schedule.frame
        if not frame or frame.is_active is False:
            # Update Schedule Status
            update_schedule_status(
                schedule_repo,
                schedule,
                ScheduleStatus.FAILED,
                message="No frame found.",
            )
            return

        response = update_profile_image(user=user, frame=frame)
        profile_image: str = response["profile_image_url_https"]
        profile_image = profile_image.replace("_normal", "_400x400")

        user_repo = UserRepository(db)
        user = user_repo.update(
            object_id=user.id, obj_in=UserUpdate(image=profile_image)
        )

        # remaining_frames -= 1
        # purchase_repo.update(
        #     object_id=purchase.id,
        #     obj_in=PurchaseUpdate(remaining_frame_usage=remaining_frames),
        # )
        update_schedule_status(
            schedule_repo,
            schedule,
            ScheduleStatus.COMPLETED,
            message="Frame Set.",
        )
    except Exception as e:
        update_schedule_status(
            schedule_repo, schedule, ScheduleStatus.FAILED, message=str(e)
        )
        raise e

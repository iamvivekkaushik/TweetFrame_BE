from typing import List
from sqlalchemy.orm import Session
from app.frame.models import Frame
from app.schedule.models import Schedule
from app.schedule.repository import ScheduleRepository
from app.user.repository import UserRepository
from sqlalchemy import func

def handle_user_stat_command(db):
    user_repo = UserRepository(db)
    total_users = user_repo.get_query().count()

    return {
        "type": 4,
        "data": {
            "content": f"Hey there! Superframes currently have `{total_users}` registered users."
        }
    }

def handle_frame_stat_command(db: Session):
    schedule_repo = ScheduleRepository(db)
    total_frames = schedule_repo.get_query().count()
    message = f">Total Frames Used: `{total_frames}`\n"

    # schedule_list: List = schedule_repo.session.query(Schedule.frame.name, func.count().label('usage')).group_by(Schedule.frame.name).all()
    query = "SELECT frame.name, COUNT(*) FROM schedule INNER JOIN frame ON schedule.frame_id=frame.id GROUP BY frame.name;"
    schedule_list = db.execute(query).fetchall()
    
    for schedule in schedule_list:
        message += f"{schedule[0]}: **{schedule[1]}**\n"

    return {
        "type": 4,
        "data": {
            "content": message
        }
    }

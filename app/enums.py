import enum


class FrameType(enum.Enum):
    FREE = "FREE"
    PREMIUM = "PREMIUM"
    CUSTOM = "CUSTOM"


class ScheduleType(enum.Enum):
    ONE_TIME = "ONE_TIME"
    RECURRING = "RECURRING"


class ScheduleStatus(enum.Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

from fastapi import APIRouter

from app.user.views import user_router
from app.plan.views import plan_router
from app.schedule.views import schedule_router
from app.purchase.views import purchase_router
from app.social_login.views import social_router
from app.frame.views import frame_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(social_router, prefix="/social_login", tags=["social_login"])
router.include_router(plan_router, prefix="/plan", tags=["plan"])
router.include_router(schedule_router, prefix="/schedule", tags=["schedule"])
router.include_router(purchase_router, prefix="/purchase", tags=["purchase"])
router.include_router(frame_router, prefix="/frame", tags=["frame"])

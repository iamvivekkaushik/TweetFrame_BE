from fastapi import APIRouter

from app.user.views import user_router
from app.plan.views import plan_router
from app.social_login.views import social_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(social_router, prefix="/social_login", tags=["social_login"])
router.include_router(plan_router, prefix="/plan", tags=["plan"])

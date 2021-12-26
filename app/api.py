from fastapi import APIRouter

from app.user import views as user_views
from app.social_login.views import social_router

router = APIRouter()

# router.include_router(user_views.auth_router, prefix="/user", tags=["User"])
# router.include_router(user_views.register_router, prefix="/user", tags=["User"])
# router.include_router(user_views.verify_router, prefix="/user", tags=["User"])
router.include_router(user_views.user_router, prefix="/user", tags=["User"])

router.include_router(social_router, prefix="/social_login", tags=["social_login"])

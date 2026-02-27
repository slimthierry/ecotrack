from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.activities import router as activities_router
from app.api.v1.challenges import router as challenges_router
from app.api.v1.achievements import router as achievements_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.reports import router as reports_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(activities_router, prefix="/activities", tags=["Activities"])
router.include_router(challenges_router, prefix="/challenges", tags=["Challenges"])
router.include_router(achievements_router, prefix="/achievements", tags=["Achievements"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
router.include_router(reports_router, prefix="/reports", tags=["Reports"])

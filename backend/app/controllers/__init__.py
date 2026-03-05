from fastapi import APIRouter

from app.controllers.auth import router as auth_router
from app.controllers.activities import router as activities_router
from app.controllers.challenges import router as challenges_router
from app.controllers.achievements import router as achievements_router
from app.controllers.dashboard import router as dashboard_router
from app.controllers.reports import router as reports_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(activities_router, prefix="/activities", tags=["Activities"])
router.include_router(challenges_router, prefix="/challenges", tags=["Challenges"])
router.include_router(achievements_router, prefix="/achievements", tags=["Achievements"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
router.include_router(reports_router, prefix="/reports", tags=["Reports"])

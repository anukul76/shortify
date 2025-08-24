from fastapi import APIRouter

from app.services.health_check.routes import router as HealthCheckRouter

router = APIRouter()


router.include_router(HealthCheckRouter, prefix="", tags=["Health-Check"])
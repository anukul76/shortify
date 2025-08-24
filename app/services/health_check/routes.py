from fastapi import APIRouter

from app.services.health_check.operations import Operations as HealthCheckOperations

router = APIRouter()
health_check_operations = HealthCheckOperations()

handlers = [
    {
        "path": "/health-check",
        "endpoint": health_check_operations.check_health,
        "methods": ["GET"]
    }
]

for route in handlers:
    router.add_api_route(
        path=route["path"],
        endpoint=route["endpoint"],
        methods=route["methods"]
    )

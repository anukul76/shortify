from fastapi import FastAPI
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.base_exception import AppException, exception_handler
from app.core.db_session import database_r, database_w
from app.routes import router
from app.core.kafka_manager import KafkaManager
from app.core.logging_config import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)


consumer_manager: KafkaManager = None

# FastAPI application instance
app = FastAPI(
    title="Service for Payment Gateway",
    description="Service for Payment Gateway",
    version=settings.release_version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(StarletteHTTPException, exception_handler)
app.add_exception_handler(AppException, exception_handler)



@app.on_event("startup")
async def startup():
    await database_r.connect()
    await database_w.connect()


@app.on_event("shutdown")
async def shutdown():
    await database_r.disconnect()
    await database_w.disconnect()


# Route Definitions
app.include_router(router, prefix="/v1")
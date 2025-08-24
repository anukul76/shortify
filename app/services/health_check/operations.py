import time
import logging
from http import HTTPStatus

from app.services.common.base import BaseOperations
from app.schemas.health_check.response_models import (
    StatusEnum,
    Health,
    DatabaseStatus,
    AppStatus,
)
from app.config import settings
from app.messages.global_messages import (
    HEALTH_CHECK_FAILED, HEALTH_CHECK_SUCCESS 
)


logger = logging.getLogger(__name__)


class Operations(BaseOperations):
    # Private Methods
    async def __db_health(self) -> DatabaseStatus:
        try:
            start: float = time.perf_counter()
            await self.db_r.execute("SELECT 1")
            elapsed_time: float = time.perf_counter() - start

            if elapsed_time > 1:
                logger.info(
                    "Database health check took longer than 1 second: %s",
                    elapsed_time,
                )

            return DatabaseStatus(
                status=StatusEnum.STATUS_UP
            )

        except Exception as exception:
            logger.warning("Database health check failed", exc_info=True)
            return DatabaseStatus(
                status=StatusEnum.STATUS_DOWN,
                error=str(exception),
            )

    async def __app_health(self) -> AppStatus:
        try:
            return AppStatus(
                status=StatusEnum.STATUS_UP, version=settings.release_version
            )

        except Exception as exception:
            return AppStatus(
                status=StatusEnum.STATUS_DOWN,
                version=settings.release_version,
                error=str(exception),
            )

    # Public Methods
    async def check_health(self):
        db_status = await self.__db_health()
        service_status = await self.__app_health()

        if (
            db_status.status is StatusEnum.STATUS_DOWN
            or service_status.status is StatusEnum.STATUS_DOWN
        ):
            return self._errorResponse(
                data=Health(database=db_status, service=service_status),
                http_status=HTTPStatus.SERVICE_UNAVAILABLE,
                message=HEALTH_CHECK_FAILED,
            )

        return self._successResponse(
            data=Health(database=db_status, service=service_status),
            http_status=HTTPStatus.OK,
            message=HEALTH_CHECK_SUCCESS,
        )

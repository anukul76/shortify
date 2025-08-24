import logging
from http import HTTPStatus
from fastapi import Request
from fastapi.responses import JSONResponse

from app.schemas.health_check.response_models import Response

logger = logging.getLogger(__name__)


class AppException(Exception):
    def __init__(
        self,
        data=None,
        message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        *args: object
    ) -> None:
        super().__init__(*args)
        self.message = message
        self.status_code = status_code
        self.data = data


async def exception_handler(request: Request, exc):
    message = getattr(
        exc, "message", getattr(exc, "detail", HTTPStatus.INTERNAL_SERVER_ERROR.phrase)
    )
    response = Response(
        success=False,
        status_code=exc.status_code,
        message=message,
        data=getattr(exc, "data", {}),
    )
    logger.error("Exception: " + exc.__class__.__name__ + "\nMessage: " + message)
    return JSONResponse(status_code=response.status_code, content=dict(response))

from enum import Enum
from http import HTTPStatus
from typing import Optional, Any
from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    STATUS_UP = "healthy"
    STATUS_DOWN = "unhealthy"


class StatusMessage(BaseModel):
    status: StatusEnum
    error: Optional[str] = None


class AppStatus(StatusMessage):
    status: StatusEnum
    error: Optional[str] = None
    version: str = Field(
        title="Application Version",
        description="Application release version",
        example="1.0.0",
    )


class DatabaseStatus(StatusMessage):
    """Status for the service's database."""
    pass


class Health(BaseModel):
    service: AppStatus
    database: StatusMessage


class Response(BaseModel):
    success: bool = Field(
        title="Response Status",
        description="Response Status",
        examples=["True"],
    )
    status_code: HTTPStatus = Field(
        title="Http status", description="Http status code", examples=[200]
    )
    message: str = Field(
        title="Response Message",
        description="Response Message",
        examples=["Data Fetched Successfully"],
    )
    data: Optional[Any] = None
    meta: Optional[dict] = None

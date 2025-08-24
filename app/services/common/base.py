import json
from http import HTTPStatus
from typing import cast, Any, List
from enum import Enum
from fastapi.responses import JSONResponse
from fastapi import Request
from app.core.db_session import database_r, database_w
from app.schemas.health_check.response_models import Response


from app.utils.base_exception import AppException


class SessionNotFound(AppException):
    pass

class ResponseStatus(str, Enum):
    
    SUCCESS = "success"
    ERROR = "error"


class BaseOperations:
    def __init__(self):
        self.db_r = database_r
        self.db_w = database_w

    def __create_json_response(self, response: Response):
        return cast(
            Any,
            JSONResponse(
                status_code=response.status_code, content=response.model_dump()
            ),
        )

    def _successResponse(
            self,
            data,
            http_status: HTTPStatus = HTTPStatus.OK,
            message: str = "Success",
            meta: dict = {}
    ) -> JSONResponse:
        response = Response(
            success=True, status_code=http_status, message=message, data=data, meta=meta
        )

        return self.__create_json_response(response)

    def _errorResponse(
            self,
            data: dict = {},
            http_status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
            message: str = "Failed",
            meta: dict = {}
    ) -> JSONResponse:
        response = Response(
            success=False, status_code=http_status, message=message, data=data, meta=meta
        )

        return self.__create_json_response(response)
    

    def paginated_response(
            self,
            items: List[Any],
            total: int,
            page: int = 1,
            per_page: int = 10,
            message: str = "Data retrieved successfully",
            http_status: HTTPStatus = HTTPStatus.OK

    ) -> JSONResponse:
        
        # Calculate pagination metadata
        total_pages = max(1, (total + per_page - 1) // per_page)
        has_next = page < total_pages
        has_prev = page > 1
        
        # Pagination metadata
        pagination_meta = {
            "pagination": {
                "current_page": page,
                "per_page": per_page,
                "total_items": total,
                "total_pages": total_pages,
                "has_next_page": has_next,
                "has_previous_page": has_prev,
                "next_page": page + 1 if has_next else None,
                "previous_page": page - 1 if has_prev else None,
                "items_on_page": len(items)
            }
        }
        response = Response(
            success=True, status_code=http_status, message=message, data=items, meta=pagination_meta
        )
        
        return self.__create_json_response(response)
    
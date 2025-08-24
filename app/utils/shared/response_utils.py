from typing import Any, Optional, Dict, List
from datetime import datetime
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
import json


class ResponseStatus(str, Enum):
    
    SUCCESS = "success"
    ERROR = "error"


class ApiResponse(BaseModel):
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True
    )
    
    status: ResponseStatus
    message: str = Field(..., min_length=1, max_length=500)
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    meta: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ResponseUtil:
    
    @staticmethod
    def _serialize_datetime(obj):
        
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    @staticmethod
    def _create_json_response(
        response_data: ApiResponse,
        status_code: int
    ) -> JSONResponse:
        
        try:
            # Convert to dict and handle datetime serialization
            content_dict = response_data.model_dump(exclude_none=True)
            content_str = json.dumps(content_dict, default=ResponseUtil._serialize_datetime)
            content = json.loads(content_str)
            
            return JSONResponse(
                status_code=status_code,
                content=content
            )
        except Exception:
            # Fallback response for serialization errors
            fallback_response = {
                "status": "error",
                "message": "Response serialization failed",
                "timestamp": datetime.utcnow().isoformat()
            }
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=fallback_response
            )
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Operation completed successfully",
        meta: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_200_OK
    ) -> JSONResponse:
        
        response_data = ApiResponse(
            status=ResponseStatus.SUCCESS,
            message=message,
            data=data,
            meta=meta
        )
        return ResponseUtil._create_json_response(response_data, status_code)
    
    @staticmethod
    def error(
        message: str = "An error occurred",
        errors: Optional[List[str]] = None,
        data: Any = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        meta: Optional[Dict[str, Any]] = None
    ) -> JSONResponse:
        
        response_data = ApiResponse(
            status=ResponseStatus.ERROR,
            message=message,
            data=data,
            errors=errors,
            meta=meta
        )
        return ResponseUtil._create_json_response(response_data, status_code)
    
    @staticmethod
    def paginated_response(
        items: List[Any],
        total: int,
        page: int = 1,
        per_page: int = 10,
        message: str = "Data retrieved successfully"
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
        
        response_data = ApiResponse(
            status=ResponseStatus.SUCCESS,
            message=message,
            data=items,
            meta=pagination_meta
        )
        return ResponseUtil._create_json_response(response_data, status.HTTP_200_OK)


# Convenience methods for common HTTP status codes with error responses
class ErrorResponses:
    
    @staticmethod
    def not_found(message: str = "Resource not found", data: Any = None) -> JSONResponse:
        
        return ResponseUtil.error(
            message=message,
            data=data,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def unauthorized(message: str = "Unauthorized access", data: Any = None) -> JSONResponse:
        
        return ResponseUtil.error(
            message=message,
            data=data,
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden(message: str = "Access forbidden", data: Any = None) -> JSONResponse:
        
        return ResponseUtil.error(
            message=message,
            data=data,
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    @staticmethod
    def validation_error(
        message: str = "Validation failed",
        errors: Optional[List[str]] = None,
        data: Any = None
    ) -> JSONResponse:
        
        return ResponseUtil.error(
            message=message,
            errors=errors,
            data=data,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    @staticmethod
    def server_error(message: str = "Internal server error", data: Any = None) -> JSONResponse:
        
        return ResponseUtil.error(
            message=message,
            data=data,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Success response methods for common HTTP status codes
class SuccessResponses:
    
    
    @staticmethod
    def created(data: Any = None, message: str = "Resource created successfully") -> JSONResponse:
        
        return ResponseUtil.success(
            data=data,
            message=message,
            status_code=status.HTTP_201_CREATED
        )
    @staticmethod
    def success(data: Any = None, message: str = "Request processed successfully") -> JSONResponse:
        
        return ResponseUtil.success(
            data=data,
            message=message,
            status_code=status.HTTP_200_OK
        )
    @staticmethod
    def accepted(data: Any = None, message: str = "Request accepted for processing") -> JSONResponse:
        
        return ResponseUtil.success(
            data=data,
            message=message,
            status_code=status.HTTP_202_ACCEPTED
        )
    
    @staticmethod
    def no_content(message: str = "Operation completed successfully") -> JSONResponse:
        
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content=None
        )


# Export all classes and main methods
__all__ = [
    'ResponseStatus',
    'ApiResponse',
    'ResponseUtil',
    'ErrorResponses',
    'SuccessResponses'
]

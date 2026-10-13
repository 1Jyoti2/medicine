"""
Common Response Envelopes and Base Schemas.
"""

import time
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")


def create_request_id() -> str:
    return f"req_{int(time.time() * 1000)}"


def datetime_now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def format_history_date() -> str:
    return time.strftime("%Y-%m-%d %H:%M")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    requestId: str = Field(default_factory=create_request_id)
    message: str = "Request completed successfully."
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    success: bool = False
    requestId: str = Field(default_factory=create_request_id)
    message: str
    detail: Optional[str] = None

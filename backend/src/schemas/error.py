"""Error response schemas."""
from typing import Optional

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    error: str = Field(
        ...,
        description="Error type/code",
    )
    message: str = Field(
        ...,
        description="Human-readable error message",
    )
    details: Optional[dict] = Field(
        None,
        description="Additional error details",
    )


class ValidationErrorResponse(BaseModel):
    """Validation error response with field-level details."""

    error: str = Field(default="validation_error")
    message: str = Field(default="Request validation failed")
    details: list[dict] = Field(
        ...,
        description="List of validation errors with field, message, and value",
    )


class NotFoundResponse(BaseModel):
    """Resource not found response."""

    error: str = Field(default="not_found")
    message: str = Field(
        ...,
        description="Resource not found message",
    )

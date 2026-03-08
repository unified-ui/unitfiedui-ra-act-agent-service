"""Response models for the agent service."""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standard error response."""

    code: str
    message: str
    details: str = ""

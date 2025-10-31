from typing import Annotated

from pydantic import BaseModel, Field


class BaseStatus(BaseModel):
    request_id: str
    request_status: str
    request_result: Annotated[str | list[str], Field(description="Request result can be a string or list of strings")]


class StatusCreatedResponse(BaseStatus):
    request_status: str = "created"
    request_result: Annotated[str | list[str], Field(description=None)] = ""


class StatusValidatedResponse(BaseStatus):
    request_status: str = "validated"
    request_result: Annotated[str | list[str], Field(description=None)] = ""


class StatusRejectedResponse(BaseStatus):
    request_status: str = "rejected"
    request_result: Annotated[str | list[str], Field(description=None)] = ""

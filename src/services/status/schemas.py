from pydantic import BaseModel


class BaseStatus(BaseModel):
    request_id: str
    request_status: str


class StatusCreatedResponse(BaseStatus):
    request_status: str = "created"


class StatusUnprocessableResponse(BaseStatus):
    request_status: str = "unprocessable"


class StatusValidatedResponse(BaseStatus):
    request_status: str = "validated"


class StatusRejectedResponse(BaseStatus):
    request_status: str = "rejected"

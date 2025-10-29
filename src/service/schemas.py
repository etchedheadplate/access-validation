from pydantic import BaseModel, field_validator


class TaskRequest(BaseModel):
    request_id: str
    request_type: str
    requested_item: str
    user_id: str
    user_groups: list[str]
    user_permissions: list[str]

    @field_validator("request_id", "request_type", "requested_item", "user_id")
    def not_empty_str(cls, v: str):
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v

    @field_validator("request_id")
    def request_id_length(cls, v: str):
        if len(v) != 22:
            raise ValueError("request_id must be 22 characters")
        return v

    @field_validator("request_type")
    def request_type_allowed(cls, v: str):
        if v not in ("group", "permission"):
            raise ValueError('request_type must be "group" or "permission"')
        return v

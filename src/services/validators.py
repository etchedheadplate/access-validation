from typing import Any

from rules import GroupRules, PermissionRules


class TaskRequestValidator:
    def __init__(self, request: dict[str, Any]):
        self.request_id = request["request_id"]
        self.request_type = request["request_type"]
        self.requested_item = request["requested_item"]
        self.user_id = request["user_id"]
        self.user_groups = set(request.get("user_groups", []))
        self.user_permissions = set(request.get("user_permissions", []))

    def validate(self) -> dict[str, Any]:
        error_msg = self._check()
        if error_msg:
            return {"request_id": self.request_id, "request_status": "rejected", "message": error_msg}
        else:
            return {
                "request_id": self.request_id,
                "request_status": "validated",
                "message": "Request validated successfully",
            }

    def _check(self) -> str | None:
        return None


class AddGroupValidator(TaskRequestValidator):
    def _check(self) -> str | None:
        updated_groups = self.user_groups | {self.requested_item}
        if any(set(forbidden) <= updated_groups for forbidden in GroupRules.CONTRADICTORY):
            return "Requested group contradicts user's groups"
        return None


class AddPermissionValidator(TaskRequestValidator):
    def _check(self) -> str | None:
        updated_groups = self.user_groups | {self.requested_item}
        if any(set(forbidden) <= updated_groups for forbidden in PermissionRules.CONTRADICTORY):
            return "Requested permission contradicts user's permissions"
        return None


def get_task_validator(request: dict[str, Any]) -> TaskRequestValidator:
    request_type = request.get("request_type")
    if request_type == "group":
        return AddGroupValidator(request)
    elif request_type == "permission":
        return AddPermissionValidator(request)
    else:
        raise ValueError(f"Unknown request type: {request_type}")

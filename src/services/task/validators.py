from typing import Any

from src.services.rules import GroupRules
from src.services.task.schemas import (
    AccessPermissionTask,
    ExcludeFromGroupTask,
    GetResourcePermissionTask,
    JoinGroupTask,
    RemovePermissionTask,
    ViewUserGroupsTask,
)


class TaskValidator:
    def __init__(self, request: dict[str, Any]):
        self.request = request
        self.request_id = request["request_id"]
        self.is_valid = False
        self.result: str | list[str] = ""

    async def validate(self) -> None:
        self.is_valid = await self._check()
        if not self.is_valid:
            self.result = "Request was not validated"

    async def _check(self) -> bool:
        return False


class JoinGroupValidator(TaskValidator):
    async def _check(self) -> bool:
        self.task = JoinGroupTask(**self.request)
        have, want = set(self.task.user_groups), self.task.group_name
        rules = GroupRules.CONTRADICTORY
        can = not any(want in rule and have & rule for rule in rules)
        return can


class AccessPermissionValidator(TaskValidator):
    async def _check(self) -> bool:
        self.task = AccessPermissionTask(**self.request)
        "TODO: logic"
        return True


class RemovePermissionValidator(TaskValidator):
    async def _check(self) -> bool:
        self.task = RemovePermissionTask(**self.request)
        "TODO: logic"
        return True


class ExcludeFromGroupValidator(TaskValidator):
    async def _check(self) -> bool:
        self.task = ExcludeFromGroupTask(**self.request)
        have, excluded_from = set(self.task.user_groups), self.task.group_name
        can = excluded_from in have
        return can


class ViewUserGroupsValidator(TaskValidator):
    async def _check(self) -> bool:
        self.task = ViewUserGroupsTask(**self.request)
        return True


class GetResourcePermissionValidator(TaskValidator):
    async def _check(self) -> bool:
        self.task = GetResourcePermissionTask(**self.request)
        "No specific logic needed"
        return True


def get_task_validator(request: dict[str, Any]) -> TaskValidator:
    type = request["request_type"]
    validator = ValidatorMapping.TASK[type]
    return validator(request)


class ValidatorMapping:
    TASK = {
        "access_permission": AccessPermissionValidator,
        "join_group": JoinGroupValidator,
        "remove_permission": RemovePermissionValidator,
        "exclude_from_group": ExcludeFromGroupValidator,
        "view_user_groups": ViewUserGroupsValidator,
        "get_resource_permission": GetResourcePermissionValidator,
    }

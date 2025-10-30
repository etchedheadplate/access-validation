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

    async def validate(self) -> None:
        is_valid = await self._check()
        self.is_valid = is_valid

    async def _check(self) -> bool:
        return False


class JoinGroupValidator(TaskValidator):
    async def _check(self) -> bool:
        self.task = JoinGroupTask(**self.request)
        updated_groups = set(self.task.user_groups) | {self.task.group_id}
        return any(set(forbidden) <= updated_groups for forbidden in GroupRules.CONTRADICTORY)


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
        "TODO: logic"
        return True


class ViewUserGroupsValidator(TaskValidator):
    async def _check(self) -> bool:
        self.task = ViewUserGroupsTask(**self.request)
        "TODO: logic"
        return True


class GetResourcePermissionValidator(TaskValidator):
    async def _check(self) -> bool:
        self.task = GetResourcePermissionTask(**self.request)
        "TODO: logic"
        return True


# class AddPermissionValidator(TaskValidator):
#    def _check(self) -> bool:
#        updated_groups = self.user_groups | {self.requested_item}
#        if any(set(forbidden) <= updated_groups for forbidden in PermissionRules.CONTRADICTORY):
#            return "Requested permission contradicts user's permissions"
#        return None


def get_task_validator(request: dict[str, Any]) -> TaskValidator:
    type = request["request_type"]
    validator = ValidatorMapping.TASK[f"{type}"]
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

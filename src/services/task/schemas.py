from pydantic import BaseModel, PositiveInt


class BaseTask(BaseModel):
    request_id: str
    error: bool = False
    request_type: str


class AccessPermissionTask(BaseTask):
    request_type: str = "access_permission"
    user_id: str
    permission_id: PositiveInt
    permission_groups: list[str]
    user_groups: list[str]


class JoinGroupTask(BaseTask):
    request_type: str = "join_group"
    user_id: str
    group_id: PositiveInt
    user_groups: list[str]
    user_permissions: list[str]


class RemovePermissionTask(BaseTask):
    request_type: str = "remove_permission"
    user_id: str
    permission_id: PositiveInt


class ExcludeFromGroupTask(BaseTask):
    request_type: str = "exclude_from_group"
    user_id: str
    group_id: PositiveInt


class ViewUserGroupsTask(BaseTask):
    request_type: str = "view_user_groups"
    user_id: str
    user_groups: list[str] = [
        "",
    ]


class GetResourcePermissionTask(BaseTask):
    request_type: str = "get_resource_permission"
    user_id: str
    resource_id: PositiveInt
    resource_permissions: list[str] = [
        "",
    ]

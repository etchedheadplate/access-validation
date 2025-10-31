from typing import Any

from src.services.status.schemas import StatusRejectedResponse, StatusValidatedResponse


class StatusProcessor:
    def __init__(self, message: dict[str, Any]):
        self.message = message
        self.request_id = message["request_id"]
        self.request_status = message["request_status"]
        self.is_appropriate = self._is_created()

    def _is_created(self) -> bool:
        return self.request_status == "created"

    async def process(self, task_validated: bool, task_result: str | list[str]):
        self.request_result = task_result
        if not task_validated:
            return StatusRejectedResponse(request_id=self.request_id, request_result=self.request_result)
        return StatusValidatedResponse(request_id=self.request_id, request_result=self.request_result)

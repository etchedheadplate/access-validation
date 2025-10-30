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

    async def process(self, valid_task: bool):
        if not valid_task:
            return StatusRejectedResponse(request_id=self.request_id)
        return StatusValidatedResponse(request_id=self.request_id)

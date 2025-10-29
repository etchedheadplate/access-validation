from service.schemas import TaskRequest
from service.validators import get_task_validator
from src.queue import EXCHANGE_NAME, ROUTING_KEY_STATUS, send_message


async def process_task_request(request_data: TaskRequest):
    validator = get_task_validator(request_data.model_dump())
    return validator.validate()


async def send_validation_result(request: TaskRequest):
    message = await process_task_request(request)
    await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, message)
    return message

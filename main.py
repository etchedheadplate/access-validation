import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import Settings
from src.logger import logger
from src.queue import RabbitMQConnection, RabbitMQConsumer
from src.worker import handle_message

settings = Settings()  # type: ignore[call-arg]
rabbit_connection = RabbitMQConnection()
consumer = RabbitMQConsumer(rabbit_connection)
exchange = settings.EXCHANGE_NAME
task_routing_key = settings.ROUTING_KEY_TASK
status_routing_key = settings.ROUTING_KEY_STATUS_CREATED


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(consumer.consume(exchange, task_routing_key, lambda msg: handle_message(msg, task_routing_key)))
    asyncio.create_task(
        consumer.consume(exchange, status_routing_key, lambda msg: handle_message(msg, status_routing_key))
    )

    yield

    await rabbit_connection.close()
    logger.info("Disconnected from RabbitMQ")


app = FastAPI(lifespan=lifespan)

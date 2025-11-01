import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.logger import logger
from src.queue import (
    EXCHANGE_NAME,
    ROUTING_KEY_STATUS,
    ROUTING_KEY_TASK,
    RabbitMQConnection,
    RabbitMQConsumer,
    RabbitMQProducer,
)
from src.worker import handle_message

rabbit_connection = RabbitMQConnection()
producer = RabbitMQProducer(rabbit_connection)
consumer = RabbitMQConsumer(rabbit_connection)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_connection.connect()
    logger.info("Connected to RabbitMQ")

    asyncio.create_task(
        consumer.consume(EXCHANGE_NAME, ROUTING_KEY_TASK, lambda msg: handle_message(msg, ROUTING_KEY_TASK))
    )
    asyncio.create_task(
        consumer.consume(EXCHANGE_NAME, ROUTING_KEY_STATUS, lambda msg: handle_message(msg, ROUTING_KEY_STATUS))
    )

    yield

    await rabbit_connection.close()
    logger.info("Disconnected from RabbitMQ")


app = FastAPI(lifespan=lifespan)

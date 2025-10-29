import asyncio
from typing import Any

from src.logger import logger
from src.queue import (
    EXCHANGE_NAME,
    ROUTING_KEY_STATUS,
    ROUTING_KEY_TASK,
    RabbitMQConnection,
    RabbitMQConsumer,
    RabbitMQProducer,
)

rabbit_connection = RabbitMQConnection()
producer = RabbitMQProducer(rabbit_connection)
consumer = RabbitMQConsumer(rabbit_connection)


async def handle_message(msg: dict[str, Any]):
    logger.info(f"Message received: {msg}")


async def main():
    await rabbit_connection.connect()

    asyncio.create_task(consumer.consume(EXCHANGE_NAME, ROUTING_KEY_TASK, handle_message))
    asyncio.create_task(consumer.consume(EXCHANGE_NAME, ROUTING_KEY_STATUS, handle_message))

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Shutting down consumers...")
    finally:
        await rabbit_connection.close()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

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


async def main():
    await rabbit_connection.connect()

    asyncio.create_task(
        consumer.consume(EXCHANGE_NAME, ROUTING_KEY_TASK, lambda msg: handle_message(msg, ROUTING_KEY_TASK))
    )
    asyncio.create_task(
        consumer.consume(EXCHANGE_NAME, ROUTING_KEY_STATUS, lambda msg: handle_message(msg, ROUTING_KEY_STATUS))
    )

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Shutting down consumers...")
    finally:
        await rabbit_connection.close()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError
from api.rest.types import ProductCreate
from core.services import product_service



logging.basicConfig(level=logging.INFO)


async def consumer_events():
    consumer = AIOKafkaConsumer(
        'product_events',
        bootstrap_servers='kafka:9093',
        group_id='product_service_group',
        auto_offset_reset='earliest',
    )

    await consumer.start()

    try:
        async for msg in consumer:
            try:
                event_data = json.loads(msg.value.decode('utf-8'))
                await handle_event(event_data)
            except KafkaError as e:
                logging.error(f"Kafka error: {e}")
    except asyncio.CancelledError:
        pass
    finally:
        await consumer.stop()

async def handle_event(event_data):
    if event_data.get("event") == "ProductCreation":
        product_data = event_data.get("product")
        if product_data:
            product_create = ProductCreate(**product_data)
            await product_service.add(product_create)
            logging.info(f"Product {product_create.id} added successfully.")
        else:
            logging.error("No product data found in the event.")
    else:
        logging.warning(f"Unknown event type: {event_data.get('event')}")
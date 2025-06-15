import json
from aiokafka import AIOKafkaProducer

producer = AIOKafkaProducer(bootstrap_servers='kafka:9093')

async def send_product_creation_event(product):
    event = {
        "event": "ProductCreation",
        "product": product.model_dump()
    }
    try:
        await producer.send_and_wait("product_events", value=json.dumps(event).encode())
        print("Message sent successfully")
    except Exception as e:
        print(f"Failed to send message: {e}")
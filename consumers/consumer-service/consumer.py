import json
import logging
import time
import pika
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


RABBIT_HOST = "rabbitmq"
EXCHANGE = "integration.exchange"
QUEUE = "analytics.queue"
ROUTING_KEY = "#"

ANALYTICS_URL = "http://analytics-service:8000/analytics/data"


# Logging setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


CUSTOMERS = {}
PRODUCTS = {}
PROCESSED_EVENTS = set()

# HTTP session with retries

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
)
session.mount("http://", HTTPAdapter(max_retries=retries))


# RabbitMQ connection

def connect_rabbitmq():
    while True:
        try:
            logger.info("🔌 Connecting to RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBIT_HOST,
                    heartbeat=60,
                    blocked_connection_timeout=300,
                )
            )
            logger.info("✅ Connected to RabbitMQ")
            return connection
        except Exception as e:
            logger.error("❌ RabbitMQ connection failed: %s", e)
            time.sleep(5)

# Message handler

def callback(ch, method, properties, body):
    try:
        event = json.loads(body.decode("utf-8"))
        event_id = event.get("eventId")

        if not event_id:
            logger.warning("⚠️ Message without eventId ignored")
            ch.basic_ack(method.delivery_tag)
            return

        if event_id in PROCESSED_EVENTS:
            logger.info("🔁 Duplicate event ignored: %s", event_id)
            ch.basic_ack(method.delivery_tag)
            return

        PROCESSED_EVENTS.add(event_id)
        routing_key = method.routing_key

        if routing_key.startswith("customer"):
            CUSTOMERS[event["id"]] = event
            logger.info("👤 Customer event received: %s", event["id"])

        elif routing_key.startswith("inventory"):
            PRODUCTS[event["id"]] = event
            logger.info("📦 Inventory event received: %s", event["id"])

        # Merge & send analytics
        for customer in CUSTOMERS.values():
            payload = {
                "customer": customer,
                "products": list(PRODUCTS.values())
            }

            response = session.post(
                ANALYTICS_URL,
                json=payload,
                timeout=5
            )

            response.raise_for_status()
            logger.info("📊 Analytics sent successfully")

        ch.basic_ack(method.delivery_tag)

    except Exception as e:
        logger.exception("🔥 Error processing message")
        ch.basic_nack(method.delivery_tag, requeue=False)


def main():
    connection = connect_rabbitmq()
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True
    )

    channel.queue_declare(queue=QUEUE, durable=True)
    channel.queue_bind(
        exchange=EXCHANGE,
        queue=QUEUE,
        routing_key=ROUTING_KEY
    )

    channel.basic_consume(
        queue=QUEUE,
        on_message_callback=callback,
        auto_ack=False
    )

    logger.info("📡 Analytics Consumer running...")
    channel.start_consuming()


if __name__ == "__main__":
    main()

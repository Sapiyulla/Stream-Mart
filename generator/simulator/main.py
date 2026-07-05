# simulator/main.py
import uuid
import json
import random
import time
from datetime import datetime, timezone
from confluent_kafka import Producer # type: ignore

# ========== CONSTANTS ==========
KAFKA_BROKER = "kafka:9092"
RUNTIME_SECONDS = 240
EVENTS_PER_SECOND = 200
SEED = 42

TOPICS = [
    "item_liked",
    "item_ordered",
    "item_clicked",
    "item_rated",
    "item_viewed",
    "item_reported",
    "item_saved",
]

CATEGORIES = [
    "electronics",
    "clothing",
    "books",
    "toys",
    "food",
    "sports",
]

REPORT_REASONS = [
    "spam",
    "inappropriate",
    "counterfeit",
    "defective",
    "misleading",
    "prohibited",
]

# ========== SETUP ==========
random.seed(SEED)

producer = Producer({"bootstrap.servers": KAFKA_BROKER})

# ========== GENERATORS (без изменений, кроме удаления value_serializer) ==========
def generate_base():
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "user_id": random.randint(1, 10_000),
            "item_id": random.randint(1, 50_000),
            "category": random.choice(CATEGORIES),
            "price": round(random.uniform(100, 50_000), 2),
        },
    }


def generate_liked():
    event = generate_base()
    event["event_type"] = "item_liked"
    return event


def generate_ordered():
    event = generate_base()
    event["event_type"] = "item_ordered"
    event["payload"]["quantity"] = random.randint(1, 5)
    return event


def generate_clicked():
    event = generate_base()
    event["event_type"] = "item_clicked"
    return event


def generate_rated():
    event = generate_base()
    event["event_type"] = "item_rated"
    event["payload"]["rating"] = random.randint(1, 5)
    return event


def generate_viewed():
    event = generate_base()
    event["event_type"] = "item_viewed"
    return event


def generate_reported():
    event = generate_base()
    event["event_type"] = "item_reported"
    event["payload"]["reason"] = random.choice(REPORT_REASONS)
    return event


def generate_saved():
    event = generate_base()
    event["event_type"] = "item_saved"
    return event


GENERATORS = {
    "item_liked": generate_liked,
    "item_ordered": generate_ordered,
    "item_clicked": generate_clicked,
    "item_rated": generate_rated,
    "item_viewed": generate_viewed,
    "item_reported": generate_reported,
    "item_saved": generate_saved,
}

# ========== MAIN ==========
def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")

def main():
    print(f"Starting generator: {RUNTIME_SECONDS}s, ~{EVENTS_PER_SECOND} events/s")
    start = time.time()
    while time.time() - start < RUNTIME_SECONDS:
        topic = random.choice(TOPICS)
        event = GENERATORS[topic]()
        producer.produce(
            topic,
            value=json.dumps(event).encode("utf-8"),
            callback=delivery_report,
        )
        producer.poll(0)
        time.sleep(1 / EVENTS_PER_SECOND)
    producer.flush()
    print(f"Done.")

if __name__ == "__main__":
    main()
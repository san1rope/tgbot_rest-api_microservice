# producer_min.py
import json, uuid
import os

from confluent_kafka import Producer

from app.config import Config

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "192.168.181.218:9092")  # ← або "localhost:9092" якщо так налаштовано
p = Producer({
    "bootstrap.servers": BOOTSTRAP,
    "enable.idempotence": True,
    "acks": "all",
    "max.in.flight.requests.per.connection": 5,
})


def send(payload: dict, topic: str = "messages") -> dict:
    """Відправляє payload у Kafka й чекає delivery-callback. Повертає метадані."""
    msg_id = payload.get("message_id") or str(uuid.uuid4())
    payload["message_id"] = msg_id

    result = {}

    def cb(err, msg):
        if err:
            result["error"] = str(err)
        else:
            result.update({
                "message_id": msg_id,
                "topic": msg.topic(),
                "partition": msg.partition(),
                "offset": msg.offset(),
            })

    p.produce(topic, key=msg_id, value=json.dumps(payload), on_delivery=cb)

    # обов'язково крутити події, поки не отримаємо callback
    while not result:
        p.poll(0.1)
    p.flush(2.0)

    if "error" in result:
        raise RuntimeError(result["error"])
    return result


if __name__ == "__main__":
    # приклад виклику
    meta = send({"chat_id": 1, "text": "hello"})
    print("OK:", meta)

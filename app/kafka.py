import json
import os
import uuid
from typing import Dict
from http import HTTPStatus

from confluent_kafka import Producer
from fastapi.responses import JSONResponse

from app.api_models import *
from app.config import Config
from app.utils import Utils as Ut


class KafkaInterface:
    BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", Config.KAFKA_BOOTSTRAP_IP)
    PRODUCER = Producer({
        "bootstrap.servers": BOOTSTRAP,
        "enable.idempotence": True,
        "acks": "all",
        "max.in.flight.requests.per.connection": 5,
    })

    @staticmethod
    async def get_request_type(payload) -> str:
        if isinstance(payload, SendMessageRequest):
            return "send_message"

        elif isinstance(payload, EditMessageRequest):
            return "edit_message"

        elif isinstance(payload, DeleteMessageRequest):
            return "delete_message"

        elif isinstance(payload, MessagePinRequest):
            return "message_pin"

        elif isinstance(payload, MessageUnpinRequest):
            return "message_unpin"

        elif isinstance(payload, SendPhotoRequest):
            return "send_photo"

        elif isinstance(payload, SendVideoRequest):
            return "send_video"

        elif isinstance(payload, SendAudioRequest):
            return "send_audio"

        elif isinstance(payload, SendDocumentRequest):
            return "send_document"

        elif isinstance(payload, SendStickerRequest):
            return "send_sticker"

        elif isinstance(payload, SendVoiceRequest):
            return "send_voice"

        elif isinstance(payload, SendGIFRequest):
            return "send_gif"

        elif isinstance(payload, CreateTopicRequest):
            return "create_topic"

        elif isinstance(payload, EditTopicRequest):
            return "edit_topic"

        elif isinstance(payload, DeleteMessageRequest):
            return "delete_topic"

        else:
            return "None"

    @classmethod
    async def send_message(cls, payload, topic: str = "messages") -> dict:
        request_type = await cls.get_request_type(payload)
        msg_id = str(uuid.uuid4())

        payload = payload.model_dump()
        payload["request_id"] = msg_id
        payload["request_type"] = request_type

        result = {}

        def callback(err, msg):
            if err:
                result["error"] = str(err)

            else:
                result.update({
                    "message_id": msg_id,
                    "topic": msg.topic(),
                    "partition": msg.partition(),
                    "offset": msg.offset(),
                })

        cls.PRODUCER.produce(topic, key=msg_id, value=json.dumps(payload), on_delivery=callback)

        while not result:
            cls.PRODUCER.poll(0.1)

        cls.PRODUCER.flush(2.0)

        return result

    @staticmethod
    async def response_from_kafka_result(result: Dict) -> JSONResponse:
        if result.get("error"):
            res_data = ResponseData(status=Ut.STATUS_FAIL, id=None, error=result.get("error"), code="TEST")
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        else:
            res_data = ResponseData(status=Ut.STATUS_SUCCESS, id=result["message_id"], error=None, code=None)
            status_code = HTTPStatus.OK

        return JSONResponse(status_code=status_code, content=res_data.model_dump())

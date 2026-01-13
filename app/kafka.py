import json
import os
import uuid
from typing import Dict
from http import HTTPStatus

from aiokafka import AIOKafkaProducer
from fastapi.responses import JSONResponse

from app.api_models import *
from app.config import Config
from app.utils import Utils as Ut


class KafkaInterface:
    BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", Config.KAFKA_BOOTSTRAP_IP)
    PRODUCER: Optional[AIOKafkaProducer] = None

    @classmethod
    async def initialize(cls):
        if cls.PRODUCER is None:
            cls.PRODUCER = AIOKafkaProducer(
                bootstrap_servers=cls.BOOTSTRAP,
                enable_idempotence=True,
                acks="all",
                max_batch_size=16384,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8")
            )
            await cls.PRODUCER.start()

    @classmethod
    async def stop(cls):
        if cls.PRODUCER:
            await cls.PRODUCER.stop()

    @staticmethod
    async def get_request_type(payload) -> str:
        mapping = {
            SendMessageRequest: "send_message",
            EditMessageRequest: "edit_message",
            DeleteMessageRequest: "delete_message",
            MessagePinRequest: "message_pin",
            MessageUnpinRequest: "message_unpin",
            SendPhotoRequest: "send_photo",
            SendVideoRequest: "send_video",
            SendAudioRequest: "send_audio",
            SendDocumentRequest: "send_document",
            SendStickerRequest: "send_sticker",
            SendVoiceRequest: "send_voice",
            SendGIFRequest: "send_gif",
            CreateTopicRequest: "create_topic",
            EditTopicRequest: "edit_topic",
        }

        for model, req_type in mapping.items():
            if isinstance(payload, model):
                return req_type

        return "None"

    @classmethod
    async def send_message(cls, payload, topic: str = "messages") -> dict:
        if cls.PRODUCER is None:
            raise RuntimeError("Kafka Producer is not initialized. Call initialize() first.")

        request_type = await cls.get_request_type(payload)
        msg_id = str(uuid.uuid4())

        data = payload.model_dump()
        data["request_id"] = msg_id
        data["request_type"] = request_type

        try:
            metadata = await cls.PRODUCER.send_and_wait(
                topic,
                key=msg_id,
                value=data
            )

            return {
                "message_id": msg_id,
                "topic": metadata.topic,
                "partition": metadata.partition,
                "offset": metadata.offset,
            }

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    async def response_from_kafka_result(result: Dict) -> JSONResponse:
        if "error" in result:
            res_data = ResponseData(
                status=Ut.STATUS_FAIL,
                id=None,
                error=result.get("error"),
                code="KAFKA_ERROR"
            )
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR

        else:
            res_data = ResponseData(
                status=Ut.STATUS_SUCCESS,
                id=result["message_id"],
                error=None,
                code=None
            )
            status_code = HTTPStatus.OK

        return JSONResponse(status_code=status_code, content=res_data.model_dump())

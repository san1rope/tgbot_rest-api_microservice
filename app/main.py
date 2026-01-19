import logging
from contextlib import asynccontextmanager
from http import HTTPStatus
from datetime import datetime

from fastapi import FastAPI, Header, Request, Depends
from fastapi.responses import JSONResponse

from app.api_models import *
from app.config import Config
from app.kafka import KafkaInterface
from app.utils import Utils as Ut


@asynccontextmanager
async def lifespan(app: FastAPI):
    datetime_of_start = datetime.now().strftime(Config.DATETIME_FORMAT)
    logger = await Ut.add_logging(datetime_of_start=datetime_of_start, process_id=0)
    Config.LOGGER = logger

    await KafkaInterface().initialize()

    yield

    await KafkaInterface.stop()


rest_app = FastAPI(lifespan=lifespan)


@rest_app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": Ut.STATUS_FAIL,
            "error": exc.error,
            "code": exc.code
        }
    )


@rest_app.post("/api/v1/messages/send", response_model=SendMessageRequest)
async def send_message(body: SendMessageRequest, authorization: str = Header(...)):
    print(f"auth token = {authorization}")
    await Ut.check_auth(authorization)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.put("/api/v1/messages/{message_id}/edit", response_model=EditMessageRequest)
async def edit_message(message_id: int, body: EditMessageRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    if message_id != body.message_id:
        raise APIError("message_id in path and body do not match", "MESSAGE_ID_MISMATCH", status_code=400)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.delete("/api/v1/messages/{message_id}", response_model=DeleteMessageRequest)
async def delete_message(message_id: int, body: DeleteMessageRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    if message_id != body.message_id:
        raise APIError("message_id in path and body do not match", "MESSAGE_ID_MISMATCH", status_code=400)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.post("/api/v1/messages/{message_id}/pin", response_model=MessagePinRequest)
async def message_pin(message_id: int, body: MessagePinRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    if message_id != body.message_id:
        raise APIError("message_id in path and body do not match", "MESSAGE_ID_MISMATCH", status_code=400)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.post("/api/v1/messages/{message_id}/unpin", response_model=MessageUnpinRequest)
async def message_unpin(message_id: int, body: MessageUnpinRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    if message_id != body.message_id:
        raise APIError("message_id in path and body do not match", "MESSAGE_ID_MISMATCH", status_code=400)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.post("/api/v1/messages/send_photo", response_model=SendPhotoRequest)
async def send_photo(body: SendPhotoRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.post("/api/v1/messages/send_video", response_model=SendVideoRequest)
async def send_video(body: SendVideoRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.post("/api/v1/messages/send_audio", response_model=SendAudioRequest)
async def send_audio(body: SendAudioRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.post("/api/v1/messages/send_document", response_model=SendDocumentRequest)
async def send_document(body: SendDocumentRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.post("/api/v1/messages/send_sticker", response_model=SendStickerRequest)
async def send_sticker(body: SendStickerRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.post("/api/v1/messages/send_voice", response_model=SendVoiceRequest)
async def send_voice(body: SendVoiceRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.post("/api/v1/messages/send_gif", response_model=SendGIFRequest)
async def send_gif(body: SendGIFRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.post("/api/v1/topics/create", response_model=CreateTopicRequest)
async def create_topic(body: CreateTopicRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.put("/api/v1/topics/{topic_id}/edit", response_model=EditTopicRequest)
async def edit_topic(topic_id: int, body: EditTopicRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    if topic_id != body.topic_id:
        raise APIError("topic_id in path and body do not match", "TOPIC_ID_MISMATCH", status_code=400)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.delete("/api/v1/topics/{topic_id}", response_model=DeleteTopicRequest)
async def delete_topic(topic_id: int, body: DeleteTopicRequest, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    if topic_id != body.topic_id:
        raise APIError("topic_id in path and body do not match", "TOPIC_ID_MISMATCH", status_code=400)

    result = await KafkaInterface().send_message(payload=body)
    return await KafkaInterface.response_from_kafka_result(result=result)


@rest_app.get("/api/v1/media/{chat_id}/{message_id}/info")
async def media_file_info(chat_id: int, message_id: int, authorization: str = Header(None)):
    await Ut.check_auth(authorization)

    # do

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=MediaFileInfoResponse(
            status=Ut.STATUS_SUCCESS,
            media_info=MediaInfo(
                file_type="str",
                file_name="asd",
                mime_type="asd",
                file_size=1000,
                width=1,
                height=1,
                created_at="datetime"
            )
        ).model_dump()
    )

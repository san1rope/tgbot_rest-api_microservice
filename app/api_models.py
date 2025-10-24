from typing import Optional

from pydantic import BaseModel


class APIError(Exception):
    def __init__(self, error: str, code: str, status_code: int = 400):
        self.error = error
        self.code = code
        self.status_code = status_code


class PhotoData(BaseModel):
    width: int
    height: int
    file_size: int


class VideoData(BaseModel):
    width: int
    height: int
    duration: int
    file_size: int


class AudioData(BaseModel):
    duration: int
    title: str
    performer: str
    file_size: int


class DocumentData(BaseModel):
    file_name: str
    mime_type: str
    file_size: int


class StickerData(BaseModel):
    width: int
    height: int
    is_animated: bool
    file_size: int


class VoiceData(BaseModel):
    duration: int
    mime_type: str
    file_size: int


class GIFData(BaseModel):
    width: int
    height: int
    duration: int
    file_size: int


class MediaInfo(BaseModel):
    file_type: str
    file_name: str
    mime_type: str
    file_size: int
    width: int
    height: int
    created_at: str


class ResponseData(BaseModel):
    status: str
    error: Optional[str]
    code: Optional[str]


class SendMessageRequest(BaseModel):
    chat_id: int
    text: str
    topic_id: int
    parse_mode: str
    disable_notification: bool
    reply_to_message_id: int


# class SendMessageResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     sent_at: str


class EditMessageRequest(BaseModel):
    chat_id: int
    message_id: int
    text: str
    parse_mode: str


# class EditMessageResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     updated_at: str
#     text: str


class DeleteMessageRequest(BaseModel):
    chat_id: int
    message_id: int


# class DeleteMessageResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     deleted_at: str


class MessagePinRequest(BaseModel):
    chat_id: int
    message_id: int


# class MessagePinResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     pinned_at: str
#     is_pinned: bool


class MessageUnpinRequest(BaseModel):
    chat_id: int
    message_id: int


# class MessageUnpinResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     unpinned_at: str
#     is_pinned: bool


class SendPhotoRequest(BaseModel):
    chat_id: int
    photo: str
    caption: str
    topic_id: int
    parse_mode: str


# class SendPhotoResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     sent_at: str
#     photo: PhotoData


class SendVideoRequest(BaseModel):
    chat_id: int
    video: str
    caption: str
    topic_id: int
    parse_mode: str


# class SendVideoResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     sent_at: str
#     video: VideoData


class SendAudioRequest(BaseModel):
    chat_id: int
    audio: str
    caption: str
    topic_id: int
    parse_mode: str


# class SendAudioResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     sent_at: str
#     audio: AudioData


class SendDocumentRequest(BaseModel):
    chat_id: int
    document: str
    caption: str
    topic_id: int
    parse_mode: str


# class SendDocumentResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     sent_at: str
#     document: DocumentData


class SendStickerRequest(BaseModel):
    chat_id: int
    sticker: str
    topic_id: int


# class SendStickerResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     sent_at: str
#     sticker: StickerData


class SendVoiceRequest(BaseModel):
    chat_id: int
    voice: str
    caption: str
    topic_id: int


# class SendVoiceResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     sent_at: str
#     voice: VoiceData


class SendGIFRequest(BaseModel):
    chat_id: int
    gif: str
    caption: str
    topic_id: int
    parse_mode: str


# class SendGIFResponse(BaseModel):
#     status: str
#     message_id: int
#     chat_id: int
#     sent_at: str
#     gif: GIFData


class CreateTopicRequest(BaseModel):
    chat_id: int
    title: str
    icon_color: int


# class CreateTopicResponse(BaseModel):
#     status: str
#     topic_id: int
#     chat_id: int
#     title: str
#     icon_color: int
#     created_at: str


class EditTopicRequest(BaseModel):
    chat_id: int
    topic_id: int
    title: str


# class EditTopicResponse(BaseModel):
#     status: str
#     topic_id: int
#     chat_id: int
#     title: str
#     updated_at: str


class DeleteTopicRequest(BaseModel):
    chat_id: int
    topic_id: int


# class DeleteTopicResponse(BaseModel):
#     status: str
#     topic_id: int
#     chat_id: int
#     deleted_at: str


class MediaFileInfoResponse(BaseModel):
    status: str
    media_info: MediaInfo

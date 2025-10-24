from app.config import Config
from app.api_models import APIError


class Utils:
    STATUS_SUCCESS = "success"
    STATUS_FAIL = "fail"

    @staticmethod
    async def check_auth(token: str):
        if not token:
            raise APIError("Missing Authorization header", "AUTH_MISSING", 401)

        if not token.startswith("Bearer "):
            raise APIError("Invalid Authorization format", "AUTH_BAD_FORMAT", 400)

        if Config.REST_API_TOKEN != token.replace("Bearer ", ""):
            raise APIError("Invalid token", "AUTH_INVALID_TOKEN", 401)

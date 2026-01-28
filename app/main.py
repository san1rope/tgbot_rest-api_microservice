import asyncio
from datetime import datetime

import uvicorn

from app.config import Config
from app.kafka import KafkaInterface
from app.utils import Utils as Ut


async def main():
    datetime_of_start = datetime.now().strftime(Config.DATETIME_FORMAT)
    logger = await Ut.add_logging(datetime_of_start=datetime_of_start, process_id=0)
    Config.LOGGER = logger

    return await KafkaInterface().initialize()


if __name__ == "__main__":
    asyncio.run(main())

    uvicorn.run(Config.REST_APP, host=Config.UVICORN_HOST, port=Config.UVICORN_PORT)

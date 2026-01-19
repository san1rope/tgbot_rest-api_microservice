import asyncio

from aiohttp import ClientSession


async def main():
    url = "http://127.0.0.1:8000/api/v1/messages/send"
    headers = {
        "Content-Type": "application/json",
        "authorization": "Bearer 21jk3h12kj3h"
    }
    data = {
        "chat_id": -1003514949333,
        "text": "message to topic",
        "topic_id": 2,
        "parse_mode": "markdown",
        "disable_notification": False,
        "reply_to_message_id": None
    }

    async with ClientSession() as session:
        async with session.post(url=url, headers=headers, json=data, timeout=10) as response:
            answer = await response.text()
            print(answer)


if __name__ == '__main__':
    asyncio.run(main())

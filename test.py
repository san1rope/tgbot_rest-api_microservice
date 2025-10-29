import asyncio

from aiohttp import ClientSession


async def main():
    url = "http://127.0.0.1:8000/api/v1/messages/send"
    headers = {
        "Content-Type": "application/json",
        "authorization": "Bearer 89e69246a5a69a8eccda9b3945457409733014f7a8a53d48b0d4b283620202ff"
    }
    data = {
        "chat_id": -1003236713326,
        "text": "hahahura",
        "topic_id": None,
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

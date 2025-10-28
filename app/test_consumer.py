import asyncio

from app.kafka import KafkaInterface


async def main():
    result = await KafkaInterface().send_message(
        payload={
            "type": "test12",
            "test": 1
        }
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())

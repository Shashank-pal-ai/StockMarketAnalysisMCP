import os
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def run_agent():
    print("hello")


if __name__ == "main":
    asyncio.run(run_agent)

import asyncio
import os
from google.antigravity import Agent, LocalAgentConfig


async def _run() -> None:
    api_key = os.environ.get("GEMINI_API_KEY")
    config = LocalAgentConfig(api_key=api_key)
    async with Agent(config) as agent:
        response = await agent.chat("Write a haiku about informal greetings.")
        print(await response.text())


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()

from workflow import SimpleEssayWorkflow, TokenEvent


async def main():
    workflow = SimpleEssayWorkflow()
    handler = workflow.run(topic="Climate Change", word_limit=100)

    async for event in handler.stream_events():
        if isinstance(event, TokenEvent):
            print(event.token, end="", flush=True)

    await handler


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

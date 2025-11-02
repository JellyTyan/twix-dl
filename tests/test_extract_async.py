from twix_dl import AsyncTwitterClient

async def main():
    client = AsyncTwitterClient()
    response = await client.get_tweet_info(2)
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

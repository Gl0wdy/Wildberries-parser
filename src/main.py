from parser import WbParser

import asyncio
import time


async def main():
    start = time.perf_counter()
    async with WbParser() as parser:
        res = await parser.search('Пальто', pages_limit=60)
        for page in res:
            for card in page:
                print(card)

    print(time.perf_counter() - start)


asyncio.run(main())
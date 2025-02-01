from parser import WbParser
from parser.constants import SortType

import asyncio
import time


async def main():
    start = time.perf_counter()
    parser = WbParser()
    res = await parser.search('Футболка белая мужская оверсайз', pages_limit=30)
    print(res.most_expensive, res.least_expensive.url)

    print(time.perf_counter() - start)


asyncio.run(main())
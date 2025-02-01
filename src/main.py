from parser import WbParser
from parser.constants import SortType

import asyncio
import time


async def main():
    start = time.perf_counter()
    parser = WbParser()
    res = await parser.search('Футболка белая мужская оверсайз', sort_type=SortType.POPULAR)
    res.globalize()

    print(time.perf_counter() - start)


asyncio.run(main())
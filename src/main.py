from parser import WbParser
from parser.utils.constants import SortType

import asyncio
import time


async def main():
    start = time.perf_counter()
    async with WbParser() as parser:
        cats = await parser.get_categories()
        res = await cats[1].childs[2].get_products(pages_limit=30)
        print(len(res.globalize()))

    print(time.perf_counter() - start)


asyncio.run(main())
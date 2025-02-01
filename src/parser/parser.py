import asyncio
from aiohttp import ClientSession
import json

from .constants import SortType
from .adapters import WbPages
        


class WbParser:
    def __init__(self):
        self.session = ClientSession()

    async def search(
            self,
            query: str,
            sort_type: SortType | str = SortType.POPULAR,
            pages_limit: int = 60
    ) -> WbPages:
        async with self.session:
            if pages_limit > 60:
                raise ValueError(f"Can't process pages_limit higher than 60 (Your value = {pages_limit})")

            url = 'https://search.wb.ru/exactmatch/ru/common/v9/search?&curr=rub&dest=-1257786&resultset=catalog'
            tasks = (
                self._make_request(url, query=query, sort=sort_type, page=page_n)
                for page_n in range(1, pages_limit + 1)
            )
            data = await asyncio.gather(*tasks)

            paginated_data = WbPages(data)
            return paginated_data
    
    async def _make_request(self, url: str, **kwargs):
        async with self.session.get(url, params=kwargs) as response:
            response.raise_for_status()

            text = await response.text()   # As some reason WB api returns text instead of JSON :/
            data = json.loads(text)
            return data
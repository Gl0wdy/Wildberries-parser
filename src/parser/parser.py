import asyncio
from aiohttp import ClientSession
import json

from .constants import SortType
from .adapters import WbPages, WbCategory
        


class WbParser:
    def __init__(self):
        self.session = None

    async def search(
            self,
            query: str,
            sort_type: SortType | str = SortType.POPULAR,
            pages_limit: int = 60
    ) -> WbPages:
        if pages_limit > 60:
            raise ValueError(f"Can't process pages_limit higher than 60 (Your value = {pages_limit})")

        url = 'https://search.wb.ru/exactmatch/ru/common/v9/search'
        tasks = (
            self._make_request(url, query=query, sort=sort_type, page=page_n, resultset='catalog')
            for page_n in range(1, pages_limit + 1)
        )
        data = await asyncio.gather(*tasks)

        paginated_data = WbPages(data)
        return paginated_data
        
    async def get_categories(self):
        response = await self._make_request(
            url='https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v2.json'
        )
        return [WbCategory(parser=self, **i) for i in response]
        
    async def get_category_products(
            self,
            category: WbCategory,
            sort_type: SortType | str = SortType.POPULAR,
            pages_limit: int = 50
    ) -> WbPages:
        tasks = (
                self._make_request(
                    url=f'https://catalog.wb.ru/catalog/{category.shard}/v2/catalog',
                    sort=sort_type, page=n, cat=category.id,
                    spp=30
                )
                for n in range(1, pages_limit + 1)
            )
        data = await asyncio.gather(*tasks)
        paginated_data = WbPages(data)
        return paginated_data
    
    async def _make_request(self, url: str, **kwargs):
        kwargs.update(
            {
                'lang': 'ru',
                'curr': 'rub',
                'ab_testing': 'false',
                'appType': '1',
                'dest': '-1257786'
            }
        )
        async with self.session.get(url, params=kwargs) as response:
            response.raise_for_status()

            text = await response.text()   # As some reason WB api returns text instead of JSON :/
            data = json.loads(text)
            return data
    
    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
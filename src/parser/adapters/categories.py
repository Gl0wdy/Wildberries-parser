from parser.utils.constants import SortType
from .common import WbKwargsInit


class WbCategory(WbKwargsInit):
    def __init__(self, parser = None, **kwargs):
        super().__init__(**kwargs)
        self._parser = parser

    async def get_products(
            self,
            sort_type: SortType | str = SortType.POPULAR,
            pages_limit: int = 50
    ):
        res = await self._parser.get_category_products(
            self,
            sort_type=sort_type,
            pages_limit=pages_limit
        )
        return res
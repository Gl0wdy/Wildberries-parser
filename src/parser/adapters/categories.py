from utils.constants import SortType


class WbCategory:
    def __init__(self, parser = None, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, list):
                setattr(self, k, [WbCategory(parser=parser, **i) for i in v])
            else:
                setattr(self, k, v)
        self.data = kwargs
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

    def __getattr__(self, name):
        try:
            return self.data[name]
        except:
            return None

    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.name}">'
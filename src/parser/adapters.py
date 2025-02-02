import asyncio

from .constants import SortType
from .utils.classes import WbIterable


class WbCard:
    '''
    Represents a WildBerries product card.
    '''

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, dict):
                setattr(self, k, WbCard(**v))
            elif isinstance(v, list):
                setattr(self, k, [WbCard(**item) if isinstance(item, dict) else item for item in v])
            else:
                setattr(self, k, v)
        self.raw = kwargs

        if (product_id := kwargs.get('id')):
            self.url = f'https://www.wildberries.ru/catalog/{product_id}/detail.aspx'
        if (sizes := kwargs.get('sizes')):
            self.price = sizes[0]['price']['product'] // 100

    def __str__(self):
        return f'<WbCard "{self.name}">' if hasattr(self, 'name') else 'Unnamed'

    def __getattr__(self, name):
        return getattr(self, name, None)
    

class WbPage(WbIterable):
    '''
    Represents a WildBerries page with products.
    '''

    def __init__(self, page: list | tuple):
        if not page:
            self.data = tuple()
            return
        
        el = page[0]
        if isinstance(el, WbCard):
            self.data = page
        elif isinstance(el, dict):
            self.data = tuple(
                WbCard(**i) for i in page
            )

    def sort(self, sort_type: SortType):
        keys = {
            SortType.PRICIUP: lambda x: x.sizes[0].price.product,
            SortType.PRICEDOWN: lambda x: -x.sizes[0].price.product,
            SortType.RATING: lambda x: x.rating
        }
        key = keys.get(sort_type)
        if not key:
            raise ValueError(f'Sort type "{sort_type}" is not available for WbPage.sort method.')

        self.cards.sort(key=key)
        return self
    
    @property
    def most_expensive(self):
        return max(
            self.data, key=lambda x: x.price
        )
    
    @property
    def least_expensive(self):
        return min(
            self.data, key=lambda x: x.price
        )


class WbPages(WbIterable):
    '''
    Represents a collection of WbPage instances.
    '''

    def __init__(self, data: list):
        try:
            self.data = tuple(
                    WbPage(page['data']['products']) for page in data
                )
        except:
            raise ValueError('"data" field invalid.')
        
    def globalize(self) -> WbPage:
        total = []
        for i in self.data:
            for card in i.data:
                total.append(card)
        
        return WbPage(total)
        
    @property
    def most_expensive(self):
        most_expensives = map(lambda x: x.most_expensive, self.data)
        return max(most_expensives, key=lambda x: x.price)
    
    @property
    def least_expensive(self):
        least_expensives = map(lambda x: x.least_expensive, self.data)
        return min(least_expensives, key=lambda x: x.price)
    

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
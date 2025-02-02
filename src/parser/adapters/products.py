from .common import WbIterable, WbKwargsInit
from parser.utils.constants import SortType


class WbCard(WbKwargsInit):
    '''
    Represents a WildBerries product card.
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if (product_id := kwargs.get('id')):
            self.url = f'https://www.wildberries.ru/catalog/{product_id}/detail.aspx'
        if (sizes := kwargs.get('sizes')):
            self.price = sizes[0]['price']['product'] // 100
    

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
class WbIterable:
    def filter(self, func):
        filtered = filter(func, self.data)
        return self.__class__(tuple(filtered))

    def __iter__(self):
        return iter(self.data)
    
    def __next__(self):
        return next(self.__iter__())
    
    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            return None
        
    def __len__(self):
        return len(self.data)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {len(self.data)}>'
    

class WbKwargsInit:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if isinstance(v, dict):
                setattr(self, k, self.__class__(**v))
            elif isinstance(v, list):
                setattr(self, k, [self.__class__(**item) if isinstance(item, dict) else item for item in v])
            else:
                setattr(self, k, v)
        self.raw = kwargs

    def __getattr__(self, name):
        return getattr(self.raw, name, None)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.name}">'
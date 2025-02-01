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
    
    def __repr__(self):
        return f'<{self.__class__.__name__} {len(self.data)}>'
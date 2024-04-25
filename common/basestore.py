from collections.abc import ItemsView
from _collections_abc import dict_keys, dict_values
from typing import Any


class BaseStore:
    '''Kind hearted dictionary'''

    def __init__(self) -> None:
        self._values: dict[str, list] = {}
        self._new_map = {}

    def keys(self) -> dict_keys:
        '''Return keys for items in store'''
        return self._values.keys()

    def values(self) -> dict_values:
        '''Return values for items in store'''
        return self._values.values()

    def items(self) -> ItemsView:
        '''Return key-value pairs for items the store'''
        return self._values.items()

    def append(self, key: str, value: Any) -> None:
        '''Append value to values for item with key key with transcoding'''
        try:
            self._values[key].append(value)
        except KeyError:
            self._values[key] = [value]
            self._new_map[key] = 0

    def extend(self, key: str, values: list) -> None:
        '''Extend item values with transcoding'''
        if len(values) == 0:
            return
        try:
            self._values[key].extend(values)
        except KeyError:
            if type(values) is not list:
                raise ValueError
            self._values[key] = values
            self._new_map[key] = 0

    def delete(self, key: str) -> None:
        '''Delete item by key'''
        del self._values[key]
        del self._new_map[key]

    def drop(self, key: str) -> None:
        '''Delete item from store'''
        del self._new_map[key]
        del self._values[key]

    def wipe(self) -> None:
        '''Clear all items from store'''
        self._new_map = {}
        self._values = {}

    def new(self, key: str) -> list:
        '''Return new values for key'''
        try:
            index = self._new_map[key]
            self._new_map[key] = len(self._values[key])
            return self._values[key][index:]
        except KeyError:
            return []

    def new_values(self) -> dict:
        '''Return a dict of new values'''
        new_values = {}
        for k in self.keys():
            new_values[k] = self.new(k)
        return new_values

    def getsizeof(self) -> int:
        '''Return length of values for all items in store'''
        sz = 0
        for v in self.values():
            sz += len(v)
        return sz

    def __getitem__(self, key: str) -> list:
        '''Get item and return empty list if does not exist'''
        assert type(key) is str
        try:
            return self._values[key]
        except KeyError:
            if type(key) is not str:
                raise TypeError
            return []

    def __setitem__(self, key: str, values: list) -> None:
        if type(key) is not str and type(values) is not list:
            raise TypeError
        self.extend(key, values)

    def __len__(self) -> int:
        '''Return number of items in store'''
        return len(self._values)

    def __str__(self):
        sz = self.getsizeof()
        b = '{0...'
        e = ': [...]}'
        return f'''datastore({b}{len(self.keys())}{e}) {sz:,}'''

    def __repr__(self):
        return self.__str__()

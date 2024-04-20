from collections.abc import ItemsView
from _collections_abc import dict_keys, dict_values
from typing import Any


class BaseStore:
    def __init__(self) -> None:
        self._values: dict[str, list] = {}

    def _transcode(self, value: Any) -> Any:
        '''Bypassed by default. Returns value unchanged'''
        return value

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
        value = self._transcode(value)
        try:
            self._values[key].append(value)
        except KeyError:
            self._values[key] = [value]

    def extend(self, key: str, values: list) -> None:
        '''Extend item values with transcoding'''
        for value in values:
            self.append(key, value)

    def delete(self, key: str) -> None:
        '''Delete item by key'''
        del self._values[key]

    def drop(self, key: str) -> None:
        '''Delete item from store'''
        del self._values[key]

    def wipe(self) -> None:
        '''Clear all items from store'''
        self._values = {}

    def getsizeof(self) -> int:
        '''Return length of values for all items in store'''
        sz = 0
        for v in self.values():
            sz += len(v)
        return sz

    def __getitem__(self, key: str) -> list:
        '''Replicates normal dictionary subscription behavior'''
        assert type(key) is str
        try:
            return self._values[key]
        except KeyError:
            return []

    def __setitem__(self, key: str, values: list) -> None:
        '''Ensures transcoding when setting item'''
        assert type(key) is str and type(values) is list
        self.extend(key, values)

    def __len__(self):
        '''Returns number of items in store'''
        return len(self._values)

    def __str__(self):
        sz = self.getsizeof()
        b = '{0...'
        e = ': [...]}'
        return f'''datastore({b}{len(self.keys())}{e}) {sz:,}'''

    def __repr__(self):
        return self.__str__()

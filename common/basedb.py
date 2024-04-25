from collections.abc import KeysView
from typing import ItemsView, Optional
import sqlite3

from milkcow.common.basestore import BaseStore


class BaseDB:
    '''Interact with database and bytes datastore'''

    def _push_by_key(self, cur, key, value) -> None:
        '''Create sql statement and executes on passed cursor'''
        assert type(value) is str, value
        sql = f'''INSERT INTO {key} VALUES (?)'''
        cur.execute(sql, [value])

    def _pull_by_key(self, key: str) -> list:
        '''Pull from database and return iterable'''
        assert type(key) is str
        sql = f'''SELECT * FROM {key}'''
        try:
            cur = self._conn.execute(sql)
            items = [value[0] for value in cur.fetchall()]
            return items
        except sqlite3.OperationalError as e:
            print(e)
        return []

    def _create_table(self, key: str) -> None:
        '''Create a database with key'''
        sql = f'''CREATE TABLE IF NOT EXISTS {key} (data TEXT NOT NULL)'''
        try:
            self._conn.execute(sql)
        except AttributeError as e:
            raise e

    def _drop_by_key(self, key: str) -> None:
        '''Drop table by key'''
        sql = f'''DROP TABLE {key};'''
        self._conn.execute(sql)

    def _push_values(self, key, values) -> None:
        '''Call _push_by_key over iterable. Does not call _prep_values'''
        assert self._conn is not None
        cur = self._conn.cursor()
        for value in values:
            self._push_by_key(cur, key, value)
        self._conn.commit()

    def connect(self, path: Optional[str] = None):
        '''Create database connection'''
        if path is None:
            self._conn = sqlite3.connect('mc.db')
        else:
            self._conn = sqlite3.connect(path)


class CachedDb(BaseDB):
    def __init__(self) -> None:
        super().__init__()
        self._new_map: dict = {}
        self._cache: BaseStore = BaseStore()

    def _add_to_cache(self, key: str, values: list) -> None:
        '''Add to cache'''
        self._cache.extend(key, values)

    def _push_values_and_cache(self, key: str, values: list) -> None:
        '''Push values and add to cache'''
        self._push_values(key, values)
        self._add_to_cache(key, values)

    def _pull_values_and_cache(self, key: str) -> list:
        '''Pull values and cache if there are any'''
        return self._pull_by_key(key)

    def new(self, key: str) -> list:
        '''Return a list of new values added since the last call'''
        return self._cache.new(key)

    def new_values(self) -> dict:
        '''Return dict of new values for all items'''
        return self._cache.new_values()

    def push(self, key: str, values: list) -> None:
        '''Push list of values to the database'''
        if key not in self._cache.keys():
            self._new_map[key] = 0
            self._create_table(key)
            self._pull_by_key(key)
        self._push_values_and_cache(key, values)

    def pull(self, key: str) -> list:
        '''Pull key from database'''
        return self._pull_values_and_cache(key)

    def drop(self, key: str) -> None:
        '''Drop form database'''
        self._drop_by_key(key)
        self._cache.drop(key)

    def keys(self) -> KeysView:
        '''Return keys for items pulled or pushed'''
        return self._cache.keys()

    def items(self) -> ItemsView:
        '''Return items pulled or pushed'''
        return self._cache.items()


class TranscodedDb(CachedDb):
    def _add_to_cache(self, key: str, values: list) -> None:
        del key
        del values
        raise NotImplementedError

    def _push_values_and_cache(self, key: str, values: list) -> None:
        del key
        del values
        raise NotImplementedError

    def _pull_values_and_cache(self, key: str) -> list:
        del key
        raise NotImplementedError

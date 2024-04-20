from typing import Optional

from milkcow.common.basestore import BaseStore


class BaseCachedDB:
    '''interact with database and bytes datastore'''

    def __init__(self, datastore: BaseStore) -> None:
        '''Construct BaseCachedDB object'''
        self._new_map: dict = {}
        self._store = datastore

    def _connect(self) -> None:
        '''Create database connection'''
        self._conn = None
        raise NotImplementedError

    def _prep_values_for_db(self, values: list) -> None:
        '''In-place operation on values list. Returns None'''
        del values
        raise NotImplementedError

    def _create_table(self, key: str) -> None:
        '''Create a database with key'''
        del key
        raise NotImplementedError

    def _push_by_key(self, cur, key, value) -> None:
        '''Create sql statement and executes on passed cursor'''
        del cur
        del key
        del value
        raise NotImplementedError

    def _pull_by_key(self, key: str) -> list:
        '''Pull from database and return iterable'''
        del key
        raise NotImplementedError

    def _drop_by_key(self, key: str) -> None:
        '''Drop table by key'''
        del key
        raise NotImplementedError

    def _push_values(self, key, values) -> None:
        '''Call _push_by_key over iterable. Does not call _prep_values'''
        assert self._conn is not None
        cur = self._conn.cursor()
        for value in values:
            self._push_by_key(cur, key, value)
        self._conn.commit()

    def push(self, key: str, values: list) -> None:
        '''Push list of values to the database'''
        if key not in self._store.keys():
            self._new_map[key] = 0
            self._create_table(key)
            self._pull_by_key(key)
        self._prep_values_for_db(values)  # modify values of list in place
        self._push_values(key, values)
        self._store.extend(key, values)

    def pull(self, key: str) -> Optional[list]:
        '''Pull from database. Will duplicate data by default'''
        values = self._pull_by_key(key)
        self._store.extend(key, values)

    def new(self, key: str):
        '''Return a list of new values since the last call'''
        assert key in self._store.keys()
        try:
            index = self._new_map[key]
        except KeyError:
            index = 0
        self._new_map[key] = len(self._store[key])
        return self._store[key][index:]

    def drop(self, key: str):
        '''Drop form database'''
        del self._new_map[key]
        self._drop_by_key(key)
        self._store.drop(key)

    def keys(self):
        '''return keys in database and in datastore'''
        return self._store.keys()

import sqlite3
from typing import Optional

from milkcow.common.basecacheddb import BaseCachedDB
from milkcow.common.basestore import BaseStore
from milkcow.common.transcode import BlobStore, ObjectStore


class BaseDB(BaseCachedDB):
    def _connect(self):
        '''Create database connection'''
        self._conn = sqlite3.connect('mc.db')

    def _prep_values_for_db(self, values: list) -> None:
        '''In-place operation on values list. Returns None'''
        del values
        raise NotImplementedError

    def _create_table(self, key: str):
        '''Create a database with key'''
        if key not in self._store.keys():
            sql = f'''CREATE TABLE IF NOT EXISTS {key} (data TEXT NOT NULL)'''
            self._conn.execute(sql)

    def _push_by_key(self, cur, key, value) -> None:
        '''Create sql statement and executes on passed cursor'''
        assert type(value) is str, value
        sql = f'''INSERT INTO {key} VALUES (?)'''
        cur.execute(sql, [value])

    def _pull_by_key(self, key: str):
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

    def _drop_by_key(self, key: str) -> None:
        '''Drop table by key'''
        sql = f'''DROP TABLE {key};'''
        self._conn.execute(sql)

    def connect(self, path: Optional[str] = None):
        '''Create database connection'''
        if path is None:
            self._connect()
        else:
            self._conn = sqlite3.connect(path)


class Db0(BaseDB):
    ''' object -> str -> db
                      -> byes -> store'''

    def __init__(self, classmodel) -> None:
        _store = BlobStore(classmodel)  # BlobStore string -> bytes'''
        super().__init__(_store)

    def _prep_values_for_db(self, values: list) -> None:
        '''Take list of objects and return list of string'''
        for i, obj in enumerate(values):
            try:
                values[i] = obj.model_dump_json()
            except Exception as e:
                try:
                    values[i] = obj.dump()
                except Exception:
                    raise e


class Db1(BaseDB):
    ''' object -> str -> db
               -> store'''

    def __init__(self, classmodel) -> None:
        self.classmodel = classmodel
        _store = BaseStore()  # BaseStore does not transcode'''
        super().__init__(_store)

    def _prep_values_for_db(self, values: list) -> None:
        '''Take list of objects and return list of string'''
        for i, obj in enumerate(values):
            assert isinstance(obj, self.classmodel)
            values[i] = obj.model_dump_json()


class Db2(BaseDB):
    ''' str -> db
            -> byes -> store'''

    def __init__(self, classmodel) -> None:
        _store = BlobStore(classmodel)  # BlobStore string -> bytes'''
        super().__init__(_store)

    def _prep_values_for_db(self, values: list) -> None:
        '''bypass'''
        x = len(values)
        del x


class Db3(BaseDB):
    ''' str -> db
            -> obj -> store'''

    def __init__(self, classmodel) -> None:
        _store = ObjectStore(classmodel)  # ObjectStore string -> objects
        super().__init__(_store)

    def _prep_values_for_db(self, values: list) -> None:
        '''bypass do nothing'''
        x = len(values)
        del x


class Db4(BaseDB):
    ''' byets -> str -> db
                     -> obj -> store'''
    pass

    def __init__(self, classmodel) -> None:
        _store = ObjectStore(classmodel)  # ObjectStore string -> objects
        super().__init__(_store)

    def _prep_values_for_db(self, values: list) -> None:
        '''Take list of bytes and do in place decode to string'''
        for i, value in enumerate(values):
            assert type(value) is bytes
            values[i] = value.decode()

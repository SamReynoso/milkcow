import json
from milkcow.common.basedb import TranscodedDb
from milkcow.core.milkcat import milkcat
from milkcow.core.senders import GetSender


def model_dump_transcoder(values: list):
    for i, obj in enumerate(values):
        try:
            values[i] = obj.model_dump_json()
        except Exception as e:
            try:
                values[i] = obj.dump()
            except Exception as d:
                print(d)
                raise e


class ObjectCow(TranscodedDb):
    ''' object -> str -> db
               -> store'''

    def __init__(self, classmodel) -> None:
        super().__init__()
        self.classmodel = classmodel

    def _add_to_cache(self, key: str, values: list) -> None:
        self._cache.extend(key, values)

    def _prep_values_for_db(self, values: list) -> None:
        '''Take list of objects and return list of string'''
        model_dump_transcoder(values)

    def _push_values_and_cache(self, key: str, values: list) -> None:
        self._add_to_cache(key, values)
        self._prep_values_for_db(values)
        self._push_values(key, values)

    def _pull_values_and_cache(self, key: str) -> list:
        values = self._pull_by_key(key)
        for i, value in enumerate(values):
            values[i] = self.classmodel(**json.loads(value))
        self._add_to_cache(key, values)
        return values

    def __str__(self) -> str:
        return f'ObjectCow(...) -> {self._cache}'

    def __repr__(self) -> str:
        return self.__str__()


class MilkCow(TranscodedDb):
    ''' object -> str -> db
                      -> bytes -> store'''

    def __init__(self, classmodel) -> None:
        super().__init__()
        self.classmodel = classmodel
        self._cache = GetSender()
        self.sender = self._cache

    def _add_to_cache(self, key: str, values: list) -> None:
        for i, value in enumerate(values):
            values[i] = value.encode()
        self._cache.extend(key, values)

    def _prep_values_for_db(self, values: list) -> None:
        model_dump_transcoder(values)

    def _push_values_and_cache(self, key: str, values: list) -> None:
        self._prep_values_for_db(values)
        self._push_values(key, values)
        self._add_to_cache(key, values)

    def _pull_values_and_cache(self, key: str) -> list:
        values = self._pull_by_key(key)
        self._add_to_cache(key, values)
        return values

    def __str__(self) -> str:
        return f'MilkCow(...) -> {self._cache}'

    def __repr__(self) -> str:
        return self.__str__()


class JqCow(TranscodedDb):
    ''' str -> db
            -> store'''

    def __init__(self, key_on: str) -> None:
        super().__init__()
        self.key_on = key_on

    def _add_to_cache(self, key: str, values: list) -> None:
        self._cache.extend(key, values)

    def _push_values_and_cache(self, key: str, values: list) -> None:
        self._push_values(key, values)
        self._add_to_cache(key, values)

    def _pull_values_and_cache(self, key: str) -> list:
        values = self._pull_by_key(key)
        self._add_to_cache(key, values)
        return values

    def push_raw_json(self, raw_json: str, ignore: bool = False) -> None:
        pylist = milkcat.load(raw_json)
        self.push_unkeyed(pylist, ignore)

    def push_unkeyed(self, pylist: list, ignore: bool = False) -> None:
        if ignore is True:
            key_map = milkcat.map_by_key_ignore_missing(self.key_on, pylist)
        else:
            key_map = milkcat.map_by_key(self.key_on, pylist)
        for k, v in key_map.items():
            self.push(k, v)

    def __str__(self) -> str:
        return f'JqCow({self.key_on}) -> {self._cache}'

    def __repr__(self) -> str:
        return self.__str__()


from typing import Optional


def dump(pylist):
    if len(pylist) > 0:
        last = pylist.pop()
        output = ''.join([sub + ", " for sub in pylist])
        output = '[' + output + last + ']\n'
        return output
    return '[]\n'


def load(raw_json: str) -> list[str]:
    c = 0
    strs = []
    cnt = 0
    sub = ''
    for c in raw_json:
        if c == '{':
            cnt += 1
        elif c == '}':
            cnt -= 1
        if cnt > 0:
            if c != ' ':
                sub += c
            if c in [':', ',']:
                sub += ' '
        elif len(sub) > 0:
            sub += c
            strs.append(''.join(sub.splitlines()))
            sub = ''
    return strs


def get_value_location(key_on: str, raw_data: str) -> tuple:
    try:
        start = raw_data.find(key_on)
        if start == -1:
            raise KeyError

        start += len(key_on) + 2
        assert start < len(raw_data)

        start = raw_data.find('"', start)
        assert start != -1

        start += 1
        assert start < len(raw_data)

        end = raw_data.find('"', start)
        assert end != -1
        return start, end
    except AssertionError:
        raise KeyError


def get_value(key_on: str, raw_data: str) -> str:
    start, end = get_value_location(key_on, raw_data)
    return raw_data[start: end]


def map_by_key(key_on: str, pylist: list) -> dict:
    key_map = {}
    for value in pylist:
        key = get_value(key_on, value)
        if key not in key_map.keys():
            key_map[key] = []
        key_map[key].append(value)
    return key_map


def map_by_key_ignore_missing(key_on: str, pylist: list) -> dict:
    key_map = {}
    for value in pylist:
        try:
            key = get_value(key_on, value)
            if key not in key_map.keys():
                key_map[key] = []
            key_map[key].append(value)
        except KeyError:
            pass
    return key_map

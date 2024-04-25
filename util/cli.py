import sys
import os
from typing import Optional

from milkcow.core.milkcat.milkcat import map_by_key_ignore_missing
from milkcow import milkcat
from milkcow import JqCow


def welcome():
    print('''milkcow is missing args:
    in_file
    key_on
    out_file''')
    sys.exit(0)


def read_stdin() -> Optional[list]:
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        pylist = milkcat.load(data)
        return pylist


def read_file(input_file):
    if os.path.isfile(input_file) is True:
        try:
            with open(input_file, 'r') as f:
                raw_json = f.read()
                return milkcat.load(raw_json)

        except Exception:
            print('read_file: Could not read file')
            sys.exit(1)

    print('FileNotFoundError')
    sys.exit(2)


def when_testing(pylist, key_on):
    map = map_by_key_ignore_missing(key_on, pylist)
    print(map)
    sys.exit(0)


def run_cli():
    args = sys.argv
    _ = args.pop(0)
    if len(args) == 0:
        welcome()
        sys.exit(0)

    pylist = read_stdin()
    if pylist is None:
        in_file = args.pop(0)
        pylist = read_file(in_file)

    if len(args) == 0:
        print('milkcow: missing key for mapping: Use -t for a test view.')
        sys.exit(1)

    key_on = args.pop(0)
    if len(args) == 0:
        if key_on == '-t':
            print(pylist)
            sys.exit(0)

        print('milkcow: Missing path to database: Use -t for a test view.')
        sys.exit(1)

    out_file = args.pop()
    if out_file == '-t':
        when_testing(pylist, key_on)
    else:
        add_to_db(key_on, pylist, out_file)


def add_to_db(key_on, pylist, out_path):
    if '-t' in sys.argv:
        print('milkcow: Can not add to db with test flag present')
        sys.exit(1)
    try:
        jqcow = JqCow(key_on)
        jqcow.connect(out_path)
        jqcow.push_unkeyed(pylist)
    except Exception:
        print('milkcow could not complete its task')
        sys.exit(1)

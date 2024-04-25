
    ███╗   ███╗██╗██╗     ██╗  ██╗ ██████╗ ██████╗ ██╗    ██╗
    ████╗ ████║██║██║     ██║ ██╔╝██╔════╝██╔═══██╗██║    ██║
    ██╔████╔██║██║██║     █████╔╝ ██║     ██║   ██║██║ █╗ ██║
    ██║╚██╔╝██║██║██║     ██╔═██╗ ██║     ██║   ██║██║███╗██║
    ██║ ╚═╝ ██║██║███████╗██║  ██╗╚██████╗╚██████╔╝╚███╔███╔╝
    ╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚══╝╚══╝ 

## v 0.0.11

## Description

A library for building middleware, local storage, and multiprocessing scripts
from python and json data using sqlite database files.

# Release Notes
## Additions
- milkcow - command line utility - A json segmentation tool.
- JqCow - Creates database entries from raw json and key word.
- ObjectCow - Creates database entries from python objects.
- milkcat - The 'parser' used for milkcow's json segmentation.
- GetSender - A SocketTransmitter factory.

### Core Features
- Automatic database creation and in-memory key-value mapping.
- Tracks the ingress of new objects.
- Performs a single level parsing of json iterables.

## Installation

```
pip install milkcow
```

## Usage
### From the command line
The milkcow command line tool provides an easy way to test out milkcow. 
Inspect milkcat's json segmentation key mapping, and push json directly to a
database on the file system.

```bash
milkcow file.json name mc.db
milkcow file.json name -t
milkcow file.json -t

cat file.json | milkcow name mc.db
```

Use the -t flag to view the segmentations output before key mapping.

```bash

milkcow file.json -t
['{"This": "is", "type": "object"}', '{"This": "is", "type": "object"}',
'{"a": "json", "type": "object"}', '{"list": "of", "type": "object"}',
'{"type": "foo"}']

```

Use the -t flag to view the key mapping output without pushing to a database.

```bash
milkcow file.json type -t
{'object': ['{"This": "is", "type": "object"}', '{"This": "is", "type": "object"}',
            '{"a": "json", "type": "object"}', '{"list": "of", "type": "object"}'],
'foo': ['{"type": "foo"}']}
```

## In a program
### ObjectCow
Creates database tables from python object. Performs simple fetch all operation
and holds objects in memory.

```python
from milkcow import ObjectCow

oc = ObjectCow(Record)

oc.push('Bob', records)
obj = oc.new('Bob')

oc.pull('Alice')
obj = oc.new('Alice')

k, v = oc.items()

for k in oc.keys()
    new = oc.new(k)
```

### MilkCow
The MilkCow holds bytes for further transmission rather than holding python
objects.

```python
from milkcow import MilkCow

mc = MilkCow(Record)
mc.pull('Bob')
mc.push('Alice', list[Record])

sender = mc.sender.new_sender()
sender = mc.sender.all_sender()
sender = mc.sender.keyed_sender('Alice')
sender.send()
```

Use the Receiver class to receive from a sender.

### JqCow
JqCow works with only raw strings, and has 2 additions to the other cow
classes.

```python
jc = JqCow('name')
jc.pull('Bob')
jc.push('Alice', records)
jc.push('Bob', records)

jc.push_unkeyed(records)
jc.push_raw_json(raw_json_list_of_objects)
```

JqCow uses the milkcat module to try to chunk raw json into a list of 'top
level json objects.'

### milkcat

```python
from milkcow import milkcat

milkcat.load(raw_json_list_of_objects)
milkcat.dump(pylist_of_strings)
```

### Receiver
in a program far away...

```python
from milkcow import Receiver
from  milkcow import SocketTransmitter

receiver = Receiver()
receiver.recv()
receiver.recv_model(Record)
receiver.new()
receiver.items()
receiver.keys()
receiver.values()
len(receiver)
receiver.getsizeof()
receiver['Bob']

receiver = Receiver(Record)
receiver.recv_model()
```

### Supported Models
Milkcow works well with pydantic models, but it also works with other classes
that can provide a valid json string. At the moment it works with pydantic or
classes that have a dump method that returns json.

This is the Record class used in all example code in this document.

```python
import json

class Record:
    name: str
    score: int
    game: int

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            assert k in self.__dict__.keys()
            self.__setattr__(k, v)
        assert type(self.name) is str
        assert type(self.score) is int
        assert type(self.game) is int

    def dump(self):
        return json.dumps(self.__dict__)
```


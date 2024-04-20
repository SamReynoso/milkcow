
    ███╗   ███╗██╗██╗     ██╗  ██╗ ██████╗ ██████╗ ██╗    ██╗
    ████╗ ████║██║██║     ██║ ██╔╝██╔════╝██╔═══██╗██║    ██║
    ██╔████╔██║██║██║     █████╔╝ ██║     ██║   ██║██║ █╗ ██║
    ██║╚██╔╝██║██║██║     ██╔═██╗ ██║     ██║   ██║██║███╗██║
    ██║ ╚═╝ ██║██║███████╗██║  ██╗╚██████╗╚██████╔╝╚███╔███╔╝
    ╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚══╝╚══╝ 

## v 0.0.01

### Description

A Tool to building middleware to backup and multiprocess data for pydantic and
json using sqlite.

### Core Features
- Creates database tables to store serialized python objects
- Can perform interprocess communication to keep long lived processes updated
- Good for piping in live data and forking to another process and saving to disk
- More to come

### Limitations
- Only supports one model class per database, atm
- You get one flavor of database query. Key -> list of objects
- Very early in development. Everything is subject to change. Still naming things
- pre-testing

## Installation
...

## Usage
### program 1
```
from milkcow import MilkCow

mc = MilkCow(Record)  # provide a model
mc.push('Bob', list[Record])  # add new objects
mc.pull('Alice)  # pull existing data by key
sender = mc.get_sender()  # create a sender
sender.send()  # send the data to a receiver
```
### program 2
In another program in the same working directory you can create a receiver
that will receive and hold objects.
```
from milkcow import Receiver

receiver = Receiver(Record)  # create a receiver
receiver.recv()  #  call 
```
You could do the samething in the python interpreter.
```
> len(receiver)
> 2
>
> for k, v in receiver.items():
>     print(k, len(v))
> Bob 80000
> Alice 80000
>
> receiver.getsizeof()
> 160000
>
> receiver['Jim']
> []

```

# Examples

To get the most from milkcow you need a pydantic model or a class with either
a model_dump_json method or a dump method. When trying to obtain a valid JSON
string, milkcow will use either of these methods. For this example I'm using a
custom class which implements a dump method.


### Import and Initialize
```
# import Record and MilkCow

from my_model_class import Record
from milkcow import MilkCow

mc = MilkCow(Record)

```

### Connect
Use connect with an existing sqlite database, or if a database doesn't exist,
one will be created at the path provided. If no path is given, milkcow will use
mc.db.
```
# Note: calling connect will not pull data into milkcows in-memory datastore

mc.connect()

# milkcow shows zero item and zero values in its datastore
output: MilkCowDB(...) -> datastore({0...0: [...]}) 0
```
We are connected, but milkcow still has no data. We need to create some before
we get started. Later we'll walk through pulling from an existing database.

### Push
We'll need to create a list of of objects of the same type we provided when
calling MilkCow(). With the list of objects we also need to specify a unique
key. Milkcow is a simple key-value store and only understands keys and lists.

```
# pseudocode
BR = [Record(**{...})] * 80_000
AR = [Record(**{...})] * 80_000

# push bob and alice
mc.push('Bob', BR)
mc.push('Alice', AR)

# outputs after each call to push
output: MilkCowDB(...) -> datastore({0...1: [...]}) 80,000
output: MilkCowDB(...) -> datastore({0...2: [...]}) 160,000
```
Pushing to the database also stores the data inside milkcow. But we cant use it
yet because its not stored in python objects. Its in bytes. This helps with the
data transmission that happens later. More about that later.

### Pull
much later...

```
# When milkcow is created, and connected, it won't pull data from the database
# on its own. It pulls any data for a key before it will push more rows, but
# other than that you need to specify the key to pull in data.

mc = MilkCowDB(Record) # new milkcow
mc.connect()
output: MilkCowDB(...) -> datastore({0...0: [...]}) 0
output: MilkCowDB(...) -> datastore({0...0: [...]}) 0


mc.pull('Bob')
output: MilkCowDB(...) -> datastore({0...1: [...]}) 80,000


mc.pull('Alice')
output: MilkCowDB(...) -> datastore({0...2: [...]}) 160,000
```
Now that we're in sync with the database we can start adding more data for Bob
and Alice. But we're going to need a way to turn the byte encodings into objects.
Milkcow comes with the get_sender method to transmit its data to a receiver in
another process. There are ways to avoid the receiver, but for this example
we'll use one.

## Transmit
Call the get_sender method on milkcow to get a SocketTransmitter that is
pre-loaded with all the new data that entered milkcow since the last sender was
created. Once the sender has sent it, it will clear its buffer to be empty. To send any
new data, you will need to get a new sender by calling get_sender on milkcow.
Senders only sting once. Like a bee. The bug.
```
sender = mc.get_sender()
output: SocketTransmitter(...) -> datastore({0...2: [...]}) 160,000
# sender is loaded with milkcows data
```

### Receive
in a program far away...

Just kidding, we're going to do this in one file. Import Process from
multiprocessing so that we can send the sender to another process and have
sender send its data back to the receiver in the main process. The receiver now
has milkcows data in the form of object. And again, there are milkcows with
datastores that will hold objects rather than byets.

```
from milkcow import Receiver
from multiprocessing import Process

sender = mc.get_sender()
receiver = Receiver(Record)
output: SocketTransmitter(...) -> datastore({0...2: [...]}) 160,000
output: Receiver(...) -> datastore({0...0: [...]}) 0

p = Process(target=sender.send, args=())
p.start()
receiver.recv()

output: SocketTransmitter(...) -> datastore({0...0: [...]}) 0 
output: Receiver(...) -> datastore({0...2: [...]}) 160,000
```


### Supporting classes
Milkcow works well with pydantic model, but it will also work with any class
that can provide a valid JSON string representation of itself. At the moment
it only works with pydantic or classes that have a dump method that returns
JSON.

# Full Example Code

### example 1) adding objects
```
from milkcow.test.example.my_model_class import Record
from milkcow import MilkCow


BOB = [Record(**{'name': 'Bob', 'score': 1, 'game': 15})] * 80_000
ALICE = [Record(**{'name': 'Alice', 'score': 1, 'game': 15})] * 80_000

conn = MilkCow(Record)
conn.connect(path='test-mc.db')
conn.push('Bob', BOB)
conn.push('Alice', ALICE)

```
### example 2) sending and receiving
```
from milkcow.test.example.my_model_class import Record
from milkcow import MilkCow, Receiver
from multiprocessing import Process


receiver = Receiver(Record)
mc = MilkCow(Record)

mc.connect(path='test-mc.db')
mc.pull('Bob')
sender = mc.get_sender()

p = Process(target=sender.send, args=())
p.start()
receiver.recv()

mc.pull('Alice')
sender = mc.get_sender()
p = Process(target=sender.send, args=())
p.start()
receiver.recv()
```

### example model - my_model_class
```
import json


class Record:
    name: str
    score: int
    game: int

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        assert type(self.name) is str
        assert type(self.score) is int
        assert type(self.game) is int

    def dump(self):
        return json.dumps(self.__dict__)

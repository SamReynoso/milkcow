
    ███╗   ███╗██╗██╗     ██╗  ██╗ ██████╗ ██████╗ ██╗    ██╗
    ████╗ ████║██║██║     ██║ ██╔╝██╔════╝██╔═══██╗██║    ██║
    ██╔████╔██║██║██║     █████╔╝ ██║     ██║   ██║██║ █╗ ██║
    ██║╚██╔╝██║██║██║     ██╔═██╗ ██║     ██║   ██║██║███╗██║
    ██║ ╚═╝ ██║██║███████╗██║  ██╗╚██████╗╚██████╔╝╚███╔███╔╝
    ╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚══╝╚══╝ 

## v 0.0.01

## Description

A Tool to building middleware for backing-up and for the multiprocessing of data
for pydantic and json using sqlite database files.

### Core Features
- Creates database tables to store serialized python objects.
- Updates long-lived processes by performing iterprocess communication.
- Facilitates the ingesting of raw data from disparate sources and move the data
  to a destination for storage and analysis.
- More to come

### Limitations
- Only supports one model class (atm) per database.
- You get one flavor of database query. Key -> list of objects
- Very early in development. Everything is subject to change. Still naming things
- pre-testing

## Installation
```
pip install milkcow
```

## Usage
### Program 1
```python
from milkcow import MilkCow

mc = MilkCow(Record)  # provide a model
mc.push('Bob', list[Record])  # add new objects
mc.pull('Alice)  # pull existing data by key
sender = mc.get_sender()  # create a sender
sender.send()  # send the data to a receiver
```
### Program 2
You can create a receiver that will receive and hold objects if you go to another
program in the same working directory.

```python
from milkcow import Receiver

receiver = Receiver(Record)  # create a receiver
receiver.recv() # receive data as model objects
```
You can do the same thing in the python interpreter.
```
> receiver.recv()
> 
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

## Examples

To get the most from milkcow you need a pydantic model or a class with either
a model_dump_json method or a dump method. When trying to obtain a valid JSON
string, milkcow will use either of these methods. For this example I'm using a
custom class which implements a dump method.


### Import and Initialize
```python
from my_model_class import Record
from milkcow import MilkCow

mc = MilkCow(Record)

```

### Connect
Use connect to connect with an existing sqlite database, or if a database
doesn't exist, one will be created at the path provided. If no path is given,
milkcow will use mc.db.
```python
mc.connect()
output: MilkCow(...) -> datastore({0...0: [...]}) 0  # empty cow
```
We are currently connected, but milkcow as yet has no data. We need to create
some data before we get started. Later we'll walk through pulling data from an
existing database.

### Push
We'll need to create a list of objects of the same type that we provided when
creating MilkCow. Along with the list of objects we also need to specify a unique
key. Milkcow is a simple key-value store and only understands keys and lists.

```python
# pseudocode
BR = [Record(**{...})] * 80_000
AR = [Record(**{...})] * 80_000

# push bob and alice
mc.push('Bob', BR)
mc.push('Alice', AR)

# outputs after each call to push
output: MilkCow(...) -> datastore({0...1: [...]}) 80,000
output: MilkCow(...) -> datastore({0...2: [...]}) 160,000
```
Pushing to the database also stores the data inside milkcow. But we can't use it
yet because it's not stored as python objects. Rather, it's bytes. This helps
with the data transmission that happens afterwards. More about that later.

### Pull
much later...

When milkcow is created, and connected, it won't pull data from the database on
its own. Well need to to specify what data to pull by providing the data's key.

```python
mc = MilkCow(Record) # new milkcow
mc.connect()
output: MilkCow(...) -> datastore({0...0: [...]}) 0
output: MilkCow(...) -> datastore({0...0: [...]}) 0


mc.pull('Bob')
output: MilkCow(...) -> datastore({0...1: [...]}) 80,000


mc.pull('Alice')
output: MilkCow(...) -> datastore({0...2: [...]}) 160,000
```
Now that we're in sync with the database we can start adding more objects for
Bob and Alice as we did before. But before we can do anything usful with the
data we're going to need a way of turning the byte encodings back into objects.

So far, we could have used the ObjectCow class rather than MilkCow. ObjectCow
holds all its data as objects, but for this example we are going to use
MilkCow's get_sender method to transmit data to a receiver in another process.

### Transmit
To get a SocketTransmitter that is pre-loaded with all the new data that entered
milkcow since the last sender was created we must call milkcow's get_sender
method. Once sender has sent the data, sender will empty its buffer. To send
new data, you will need to get a new sender by calling get_sender again. Senders
only sting once. Much like the bee, a bug.
```python
sender = mc.get_sender()
output: SocketTransmitter(...) -> datastore({0...2: [...]}) 160,000
# sender is loaded with milkcows data
```

### Receive
in a program far away...

Just kidding, we're going to do this in one file. We must import Process from
multiprocessing so that we can send the sender to another process and have
sender send its data back to the receiver in the main process. The receiver now
has milkcow's data in the form of objects.

```python
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

### Supported Models
Milkcow works well with pydantic models, but it will also work with any class
that can provide a valid JSON string representation of itself. At the moment
it only works with pydantic or classes that have a dump method that returns
JSON.

## Full Example Code

### example 1) adding objects
```python
from milkcow.test.example.my_model_class import Record
from milkcow import MilkCow


BOB = [Record(**{'name': 'Bob', 'score': 1, 'game': 15})] * 80_000
ALICE = [Record(**{'name': 'Alice', 'score': 1, 'game': 15})] * 80_000

mc = MilkCow(Record)
mc.connect(path='test-mc.db')
mc.push('Bob', BOB)
mc.push('Alice', ALICE)

```
### example 2) sending and receiving
```python
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

### example model) my_model_class
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

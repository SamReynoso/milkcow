from milkcow.core.connections import Db0, Db1
from milkcow.core.basebufferedsocket import BaseBuffedSocket
from milkcow.common.transcode import ReceiverStore


class SocketTransmitter(BaseBuffedSocket):
    def __init__(self):
        self._self_delete_on_send = True
        super().__init__()

    def send(self):
        super().send()
        if self._self_delete_on_send is True:
            self.wipe()

    def extend(self, key: str, values) -> None:
        '''Extend values in buffer'''
        self._buffer.extend(key, values)

    def items(self):
        '''Return items in buffer'''
        return self._buffer.items()

    def wipe(self):
        '''Clear buffer'''
        self._buffer.wipe()

    def __str__(self):
        return f'SocketTransmitter(...) -> {self._buffer}'

    def __repr__(self):
        return self.__str__()


class MilkCow(Db0):
    def get_sender(self):
        '''Return SocketTransmitter with new data in its buffer'''
        sender = SocketTransmitter()
        sender._self_delete_on_send = True
        for k in self.keys():
            values = self.new(k)
            sender.extend(k, values)
        return sender

    def __str__(self):
        return f'MilkCow(...) -> {self._store}'

    def __repr__(self):
        return self.__str__()


class ObjectCow(Db1):
    def __str__(self):
        return f'ObjectCow(...) -> {self._store}'

    def __repr__(self):
        return self.__str__()


class Receiver(ReceiverStore):
    def recv(self):
        '''recv classmodel objects into self'''
        buffer = SocketTransmitter()
        buffer.recv()
        for k, v in buffer.items():
            self.extend(k, v)

    def __str__(self):
        return f'Receiver(...) -> {super().__str__()}'

    def __repr__(self):
        return self.__str__()

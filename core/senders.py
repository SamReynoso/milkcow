
from collections.abc import ItemsView
import json
from typing import Any, Optional
from milkcow.common.basebufferedsocket import BaseBuffedSocket
from milkcow.common.basestore import BaseStore


class SocketTransmitter(BaseBuffedSocket):
    def __init__(self):
        self._self_delete_on_send = True
        super().__init__()

    def send(self) -> None:
        '''Send data in self'''
        super().send()
        if self._self_delete_on_send is True:
            self.wipe()

    def extend(self, key: str, values) -> None:
        '''Extend values in buffer'''
        self._buffer.extend(key, values)

    def items(self) -> ItemsView:
        '''Return items in buffer'''
        return self._buffer.items()

    def wipe(self) -> None:
        '''Clear buffer'''
        self._buffer.wipe()

    def __str__(self) -> str:
        return f'SocketTransmitter(...) -> {self._buffer}'

    def __repr__(self) -> str:
        return self.__str__()


class GetSender(BaseStore):
    '''SocketTransmitter factory'''

    def __init__(self, delete_on_send=True):
        super().__init__()
        self.delete_on_send = delete_on_send

    def _get_key_sender(self, key: str) -> SocketTransmitter:
        '''Create SocketTranmitter with values of key'''
        sender = SocketTransmitter()
        sender._self_delete_on_send = self.delete_on_send
        sender.extend(key, self[key])
        return sender

    def _get_keys_sender(self, keys: list) -> SocketTransmitter:
        '''Create SocketTranmitter with values of keys'''
        sender = SocketTransmitter()
        sender._self_delete_on_send = self.delete_on_send
        for key in keys:
            sender.extend(key, self[key])
        return sender

    def keyed_sender(self, keys_of_key: list | str) -> SocketTransmitter:
        '''Create SocketTranmitter with values of key or keys'''
        if type(keys_of_key) is str:
            return self._get_key_sender(keys_of_key)
        if type(keys_of_key) is list:
            return self._get_keys_sender(keys_of_key)
        raise TypeError

    def new_sender(self) -> SocketTransmitter:
        '''Return SocketTransmitter with new data in its buffer'''
        sender = SocketTransmitter()
        sender._self_delete_on_send = self.delete_on_send
        for k in self.keys():
            values = self.new(k)
            sender.extend(k, values)
        return sender

    def all_sender(self) -> SocketTransmitter:
        '''Return SocketTransmitter with key data in its buffer'''
        sender = SocketTransmitter()
        sender._self_delete_on_send = self.delete_on_send
        for k, v in self.items():
            sender.extend(k, v)
        return sender

    def __str__(self) -> str:
        return f'GetSender(...) -> {super().__str__()}'

    def __repr__(self) -> str:
        return self.__str__()


class Receiver(BaseStore):
    def __init__(self, classmodel: Optional[Any] = None):
        super().__init__()
        self.classmodel = classmodel

    def recv(self) -> None:
        '''Receives raw data into self'''
        buffer = SocketTransmitter()
        buffer.recv()
        for k, v in buffer.items():
            self.extend(k, v)

    def recv_model(self, classmodel=None) -> None:
        '''Receives bytes and creates class instances'''
        if classmodel is not None:
            model = classmodel
        model = self.classmodel
        if model is None:
            print('model must be given at function call or object creation')
            raise ValueError
        if classmodel is not None:
            model = classmodel
        buffer = SocketTransmitter()
        buffer.recv()
        for k, v in buffer.items():
            for i, data in enumerate(v):
                v[i] = model(**json.loads(data.decode()))
            self.extend(k, v)

    def __str__(self) -> str:
        return f'Receiver(...) -> {super().__str__()}'

    def __repr__(self) -> str:
        return self.__str__()

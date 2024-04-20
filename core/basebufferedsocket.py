import os
import time
import socket
from typing import Optional

from milkcow.common.basestore import BaseStore


class BaseBuffedSocket:

    def __init__(self):
        self._buffer = BaseStore()
        self._path = 'socket'

    def _close(self, uni: socket.socket) -> None:
        '''close socket'''
        uni.close()
        try:
            os.unlink(self._path)
        except OSError:
            if os.path.exists(self._path):
                raise OSError

    def _bind(self) -> socket.socket:
        '''creates socket'''
        try:
            os.unlink(self._path)
        except OSError:
            if os.path.exists(self._path):
                raise OSError
        uni = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        uni.bind(self._path)
        return uni

    def _connect(self) -> Optional[socket.socket]:
        '''Return socket connection'''
        uni = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        count = 0
        if os.path.exists(self._path):
            try:
                uni.connect(self._path)
                return uni
            except ConnectionRefusedError:
                if count == 3:
                    print('uni_connect: ConnectionRefusedError: exiting')
                    return
        if count == 2:
            print("File descriptor at 'path' does not exists")
            return
        count += 1
        time.sleep(1)

    def _send_buffer(self, uni: socket.socket) -> None:
        '''Send data in buffer'''
        for key, values in self._buffer.items():
            cnt = 0
            while cnt < len(values):
                uni.send('pad_end'.encode())
                uni.send(key.encode())
                for e in range(60):
                    if cnt < len(values):
                        uni.send(values[e])
                    else:
                        uni.send('none'.encode())
                    cnt += 1
        uni.send('done'.encode())

    def _recv_buffer(self, uni: socket.socket) -> bool:
        '''accumulates sent messages'''
        msg = uni.recv(1024).decode()
        buffer = []
        if msg == 'pad_end':
            key = uni.recv(1024).decode()
            for _ in range(60):
                data = uni.recv(1024)
                buffer.append(data)
            while buffer[-1].decode() == 'none':
                buffer.pop()
            self._buffer.extend(key, buffer)
            return True
        elif msg == 'done':
            return False
        raise ValueError

    def set_path(self, path: str) -> None:
        '''Set path to socket file descriptor. Default is 'socket' '''
        self._path = path

    def send(self):
        '''Calling function for related send functions'''
        uni = self._connect()
        if uni is not None:
            self._send_buffer(uni)
            self._close(uni)

    def recv(self, timeout=3) -> None:
        '''Create socket connection and waits for transition completion before
        closure'''
        uni = self._bind()
        uni.settimeout(timeout)
        try:
            while True:
                run = self._recv_buffer(uni)
                if run is False:
                    break
        except Exception as e:
            print(e)

import json

from milkcow.common.basestore import BaseStore


class BaseModelStore(BaseStore):
    def __init__(self, classmodel):
        '''Take class at initialization for transcoding'''
        super().__init__()
        self.classmodel: type = classmodel


class BlobStore(BaseModelStore):
    def _transcode(self, value: str):
        '''Encode string into bytes'''
        assert type(value) is str, value
        return value.encode()


class ObjectStore(BaseModelStore):
    def _transcode(self, value: str):
        '''Encode string into pydantic model'''
        assert type(value) is str
        return self.classmodel(**json.loads(value))


class ReceiverStore(BaseModelStore):
    def _transcode(self, value: str):
        '''Encode bytes into class instance'''
        assert type(value) is bytes
        try:
            return self.classmodel(**json.loads(value.decode()))
        except Exception as e:
            print(value)
            raise e

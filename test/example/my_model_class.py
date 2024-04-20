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

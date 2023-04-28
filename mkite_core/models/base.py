import os
import uuid
import json
import msgspec as msg
from typing import List, BinaryIO
from datetime import datetime


class BaseInfo(msg.Struct):
    @classmethod
    def from_json(cls, path: os.PathLike):
        with open(path, "rb") as f:
            data = f.read()

        return msg.json.decode(data, type=cls)

    def encode(self):
        return msg.json.encode(self)

    def to_json(self, path: os.PathLike):
        with open(path, "wb") as f:
            f.write(self.encode())

    def as_dict(self):
        fields = {}
        for f in self.__struct_fields__:
            value = getattr(self, f)
            fields[f] = value.as_dict() if isinstance(value, BaseInfo) else value

        return {
            **fields,
            **self.extra_dict_fields,
        }

    @property
    def extra_dict_fields(self):
        return {}

    @classmethod
    def from_dict(cls, data: dict):
        internal_data = {f: data[f] for f in cls.__struct_fields__}
        return cls(**internal_data)

    @classmethod
    def decode(cls, data: BinaryIO):
        decoder = msg.json.Decoder(cls)
        return decoder.decode(data)

    def copy(self):
        cls = self.__class__
        return cls.from_dict(self.as_dict())

    def create_uuid(self):
        return str(uuid.uuid4())


class NodeResults(BaseInfo):
    chemnode: dict
    calcnodes: List[dict] = []

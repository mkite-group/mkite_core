import collections.abc
from pydantic import FilePath, BaseModel


class BaseOptions(BaseModel):
    @staticmethod
    def dict_update(d, u):
        if isinstance(u, BaseModel):
            u = u.model_dump()

        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = BaseOptions.dict_update(d.get(k, {}), v)
            else:
                d[k] = v
        return d

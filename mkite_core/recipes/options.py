import collections.abc
from pydantic import FilePath, BaseModel


class BaseOptions(BaseModel):
    @staticmethod
    def dict_update(d, u):
        if isinstance(u, BaseModel):
            u = u.model_dump()

        if isinstance(d, BaseModel):
            new = d.model_dump()
        else:
            new = d.copy()

        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                new[k] = BaseOptions.dict_update(new.get(k, {}), v)
            else:
                new[k] = v

        return new

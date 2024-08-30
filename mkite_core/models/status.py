from enum import Enum


class Status(Enum):
    BUILDING = "building"
    READY = "ready"
    DOING = "doing"
    DONE = "done"
    ERROR = "error"
    PARSING = "parsing"
    ANY = "any"
    ARCHIVE = "archive"

    @classmethod
    def values(cls):
        return {k.value for k in Status}

    @classmethod
    def has_value(cls, value):
        return value in cls.values()

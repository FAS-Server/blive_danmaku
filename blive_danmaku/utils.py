from mcdreforged.api.rtext import RTextBase
from typing import Union
from mcdreforged.api.types import ServerInterface


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance


def print_msg(message: Union[str, RTextBase]):
    try:
        ServerInterface.get_instance().say(message)
    except AttributeError:
        print(message)

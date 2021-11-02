from mcdreforged.api.rtext import RTextBase
from typing import Union
from mcdreforged.api.types import ServerInterface


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    @classmethod
    def get_instance(cls):
        return cls._instance


def print_msg(message: Union[str, RTextBase]):
    try:
        server = ServerInterface.get_instance().broadcast(message)
    except:
        print(message)

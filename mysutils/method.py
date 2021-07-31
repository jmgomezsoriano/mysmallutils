from threading import Lock
from typing import Callable


def synchronized(method: Callable) -> Callable:
    """ Function decorator to synchronize a method.

    :param method: The method.
    :return: The synchronized method.
    """
    outer_lock = Lock()
    lock_name = "__" + method.__name__ + "_lock" + "__"

    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name):
                setattr(self, lock_name, Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)

    return sync_method

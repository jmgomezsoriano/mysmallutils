import threading
from enum import Enum
from queue import Queue
from typing import Callable, Any


class ArgsMode(Enum):
    ITEM = 0
    ARGS = 1
    KWARGS = 2


class _Finished(object):
    pass


class CallableQueueThread(threading.Thread):
    def __init__(self, func: Callable, args_mode: ArgsMode = ArgsMode.ITEM, **kwargs) -> None:
        """ A FIFO queue to run the callable when an item is introduced or while the queue had elements.

        :param func: The callable function to call for each queue element.
        :param args_mode: How the queue elements will be passed to the callable:
            ArgsTypes.ITEM pass the element as a single parameter (item);
            ArgsTypes.ARGS pass the element as a list of parameters (*item);
            ArgsTypes.KWARGS pass the element a dictionary of named parameters (**item).
        :param kwargs: The rest of Thread constructor parameters.
        """
        super().__init__(**kwargs)
        self.__args_type = args_mode
        self.__func = func  # Callable to execute on each queue item
        self.__queue = Queue()  # Queue to store elements
        self.__stop_event = threading.Event()  # Event to signal when to stop the threads
        self.__wait = False  # If the queue has to wait to process all the elements before to finish

    def run(self) -> None:
        """ Run this thread. """
        while not self.__stop_event.is_set() or self.__wait:
            # Safely retrieve an item from the queue
            item = self.pop()
            self.__wait = False if self.__queue.empty() else self.__wait
            if not isinstance(item, _Finished) and not self.__stop_event.is_set() or self.__wait:
                if self.__args_type == ArgsMode.ITEM:
                    self.__func(item)
                elif self.__args_type == ArgsMode.ARGS:
                    self.__func(*item)
                elif self.__args_type == ArgsMode.KWARGS:
                    self.__func(**item)
                else:
                    raise ValueError(f'Invalid value for args_type: {self.__args_type}. '
                                     f'Valid values: ArgsTypes.ITEM, ArgsTypes.ARGS, ArgsTypes.KWARGS')

    def add(self, item: Any) -> None:
        """ Add an item to the queue and wake up a worker thread if necessary.

        :param item: The element to add to the queue.
        """
        if self.__wait:
            raise IndexError(f'You cannot add more elements if you are waiting to finish')
        if not self.__stop_event.is_set():
            self.__queue.put(item)  # Add the item to the queue

    def pop(self) -> Any:
        """ Remove and return the item at the front of the queue.

        :return: The removed element.
        """
        return self.__queue.get()

    def wait(self) -> None:
        """ Stop the process waiting to empty the queue. """
        self.__wait = True
        self.stop()
        self.join()

    def stop(self) -> None:
        """ Signal the workers to stop processing and exit. """
        self.__stop_event.set()  # Set the stop event
        # self.__queue.join()
        self.__queue.put(_Finished())

    def __enter__(self) -> 'CallableQueueThread':
        # Start the thread
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Stop the thread
        self.wait()

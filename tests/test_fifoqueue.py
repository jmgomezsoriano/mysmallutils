import threading
import time
import unittest
from random import uniform

from mysutils.collections import CallableQueueThread, ArgsMode

GLOBAL = []


def func(a: int, b: str = 'a'):
    GLOBAL.append((a, b))


def add_to_queue(queue, num):
    time.sleep(uniform(0, 1))  # Random wait
    queue.add(num)


class MyTestCase(unittest.TestCase):
    def test_item_parameter(self):
        GLOBAL.clear()
        self.assertListEqual(GLOBAL, [])
        queue = CallableQueueThread(func)
        queue.start()
        try:
            threads = []
            for i in range(100):
                thread = threading.Thread(target=add_to_queue, args=(queue, i))
                thread.start()
                threads.append(thread)

            # Wait to finish the threads
            for thread in threads:
                thread.join()
            time.sleep(1)  # This is necessary to be sure that the last has time to finish
            # Check the results
            s = {(i, 'a') for i in range(100)}
            self.assertEqual(s, set(GLOBAL))
        finally:
            queue.stop()
            queue.join()

    def test_args_parameters(self):
        GLOBAL.clear()
        self.assertListEqual(GLOBAL, [])
        queue = CallableQueueThread(func, ArgsMode.ARGS)
        queue.start()
        try:
            threads = []
            for i in range(100):
                thread = threading.Thread(target=add_to_queue, args=(queue, (i, 'b')))
                thread.start()
                threads.append(thread)

            # Wait to finish the threads
            for thread in threads:
                thread.join()
            queue.wait()  # This is necessary to be sure that the last has time to finish
            # Check the results
            s = {(i, 'b') for i in range(100)}
            self.assertEqual(s, set(GLOBAL))
        finally:
            queue.stop()
            queue.join()

    def test_kwargs_parameters(self):
        GLOBAL.clear()
        queue = CallableQueueThread(func, ArgsMode.KWARGS)
        queue.start()
        try:
            threads = []
            for i in range(100):
                thread = threading.Thread(target=add_to_queue, args=(queue, {'a': i, 'b': 'c'}))
                thread.start()
                threads.append(thread)

            # Wait to finish the threads
            for thread in threads:
                thread.join()
            queue.wait()  # This is necessary to be sure that the last has time to finish
            # Check the results
            s = {(i, 'c') for i in range(100)}
            self.assertEqual(s, set(GLOBAL))
        finally:
            queue.stop()
            queue.join()

    def test_with_item_parameter(self):
        GLOBAL.clear()
        with CallableQueueThread(func) as queue:
            threads = []
            for i in range(100):
                thread = threading.Thread(target=add_to_queue, args=(queue, i))
                thread.start()
                threads.append(thread)

            # Wait to finish the threads
            for thread in threads:
                thread.join()
            queue.wait()  # This is necessary to be sure that the last has time to finish
            # Check the results
            s = {(i, 'a') for i in range(100)}
            self.assertEqual(s, set(GLOBAL))

    def test_with_args_parameters(self):
        GLOBAL.clear()
        with CallableQueueThread(func, ArgsMode.ARGS) as queue:
            threads = []
            for i in range(100):
                thread = threading.Thread(target=add_to_queue, args=(queue, (i, 'b')))
                thread.start()
                threads.append(thread)

            # Wait to finish the threads
            for thread in threads:
                thread.join()
            queue.wait()  # This is necessary to be sure that the last has time to finish
            # Check the results
            s = {(i, 'b') for i in range(100)}
            self.assertEqual(s, set(GLOBAL))

    def test_with_kwargs_parameters(self):
        GLOBAL.clear()
        with CallableQueueThread(func, ArgsMode.KWARGS) as queue:
            threads = []
            for i in range(100):
                thread = threading.Thread(target=add_to_queue, args=(queue, {'a': i, 'b': 'c'}))
                thread.start()
                threads.append(thread)

            # Wait to finish the threads
            for thread in threads:
                thread.join()
            queue.wait()  # This is necessary to be sure that the last has time to finish
            # Check the results
            s = {(i, 'c') for i in range(100)}
            self.assertEqual(s, set(GLOBAL))

    def test_simple_sequencial(self):
        GLOBAL.clear()
        with CallableQueueThread(func) as queue:
            for i in range(20):
                queue.add(i)  # Call func(i) from i=1 to 99, executing sequentially
        self.assertListEqual(GLOBAL, [(i, 'a') for i in range(20)])
        GLOBAL.clear()
        with CallableQueueThread(func, ArgsMode.ARGS) as queue:
            for i in range(20):
                queue.add((i, 'b'))  # Call func(i, 'b') from i=1 to 99, executing sequentially
        self.assertListEqual(GLOBAL, [(i, 'b') for i in range(20)])
        GLOBAL.clear()
        with CallableQueueThread(func, ArgsMode.KWARGS) as queue:
            for i in range(20):
                queue.add({'a': i, 'b': 'c'})  # Call func(a=i, b='c') from i=1 to 99, executing sequentially
        self.assertListEqual(GLOBAL, [(i, 'c') for i in range(20)])


if __name__ == '__main__':
    unittest.main()

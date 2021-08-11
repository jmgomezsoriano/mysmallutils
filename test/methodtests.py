import unittest
from time import sleep
from threading import Thread

from mysutils.method import synchronized


num = 0


class MyClass(object):
    @synchronized
    def calculate(self):
        global num
        print(f'Starting calculation {num}.')
        sleep(5)
        num += 1
        print(f'Ending calculation {num}.')


class MyTestCase(unittest.TestCase):
    def test_method_synchronization(self):
        obj1, obj2 = MyClass(), MyClass()
        thread = Thread(target=obj1.calculate)
        thread.start()
        sleep(1)
        print('Starting the obj2')
        obj2.calculate()
        self.assertEqual(num, 2)  # add assertion here


if __name__ == '__main__':
    unittest.main()

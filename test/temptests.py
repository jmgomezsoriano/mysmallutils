from mysutils import unittest
from mysutils.file import touch, remove_files, mkdirs
from mysutils.tmp import removable_tmp, removable_files


class MyTestCase(unittest.FileTestCase):
    def test_removable_files(self) -> None:
        touch('1.txt', '2.txt', '3.txt', 'x.out', 'y.out', 'z.out')
        with removable_files('1.txt', '2.txt', '3.txt', 'x.out', 'y.out', 'z.out'):
            self.assertExists('1.txt', '2.txt', '3.txt', 'x.out', 'y.out', 'z.out')
        self.assertNotExists('1.txt', '2.txt', '3.txt', 'x.out', 'y.out', 'z.out')

    def test_remove_recursively(self) -> None:
        with removable_files('data2', recursive=True):
            mkdirs('data1', 'data2')
            touch('data1/1.txt', 'data1/2.txt', 'data1/3.txt', 'data2/1.txt', 'data2/2.txt', 'data2/3.txt')
            self.assertExists('data1/1.txt', 'data1/2.txt', 'data1/3.txt', 'data2/1.txt', 'data2/2.txt', 'data2/3.txt')
            with self.assertRaises(OSError):
                remove_files('data1')
            remove_files('data1', recursive=True)
            self.assertNotExists('data1')
        self.assertNotExists('data2')

    def test_removable_tmp(self) -> None:
        with removable_tmp() as tmp:
            touch(tmp)
            self.assertExists(tmp)
        self.assertNotExists(tmp)

    def test_assign_removable_files(self) -> None:
        with removable_files(*touch('1.txt', '2.txt', '3.txt')) as (f1, f2, f3):
            self.assertExists(f1, f2, f3)
        self.assertNotExists(f1, f2, f3)


if __name__ == '__main__':
    unittest.main()

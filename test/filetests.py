import unittest
from os import remove, rmdir
from os.path import exists

from mysutils.command import execute_command
from mysutils.file import save_json, load_json, save_pickle, load_pickle, copy_files
from mysutils.yaml import load_yaml, save_yaml


class FileTestCase(unittest.TestCase):
    def test_json(self) -> None:
        d = {
            'version': 1.0,
            'file_list': ['1.txt', '2.txt']
        }
        save_json(d, 'test1.json')
        d2 = load_json('test1.json')
        self.assertDictEqual(d, d2)
        remove('test1.json')
        save_json(d, 'test1.json.gz')
        d2 = load_json('test1.json.gz')
        self.assertDictEqual(d, d2)
        remove('test1.json.gz')
        with self.assertRaises(FileNotFoundError):
            save_json(d, 'data/test1.json')
        with self.assertRaises(FileNotFoundError):
            save_json(d, 'data/test1.json.gz')
        save_json(d, 'data/test1.json', force=True)
        d2 = load_json('data/test1.json')
        self.assertDictEqual(d, d2)
        remove('data/test1.json')
        rmdir('data/')
        save_json(d, 'data/test1.json.gz', force=True)
        d2 = load_json('data/test1.json.gz')
        self.assertDictEqual(d, d2)
        remove('data/test1.json.gz')
        rmdir('data/')

    def test_pickle(self) -> None:
        d = {
            'version': 1.0,
            'file_list': ['1.txt', '2.txt']
        }
        save_pickle(d, 'test1.pkl')
        d2 = load_pickle('test1.pkl')
        self.assertDictEqual(d, d2)
        remove('test1.pkl')
        save_pickle(d, 'test1.pkl.gz')
        d2 = load_pickle('test1.pkl.gz')
        self.assertDictEqual(d, d2)
        remove('test1.pkl.gz')
        with self.assertRaises(FileNotFoundError):
            save_pickle(d, 'data/test1.pkl')
        with self.assertRaises(FileNotFoundError):
            save_pickle(d, 'data/test1.pkl.gz')
        save_pickle(d, 'data/test1.pkl', force=True)
        d2 = load_pickle('data/test1.pkl')
        self.assertDictEqual(d, d2)
        remove('data/test1.pkl')
        rmdir('data/')
        save_pickle(d, 'data/test1.pkl.gz', force=True)
        d2 = load_pickle('data/test1.pkl.gz')
        self.assertDictEqual(d, d2)
        remove('data/test1.pkl.gz')
        rmdir('data/')

    def test_yaml(self) -> None:
        d = {
            'version': 1.0,
            'file_list': ['1.txt', '2.txt']
        }
        save_yaml(d, 'test1.pkl')
        d2 = load_yaml('test1.pkl')
        self.assertDictEqual(d, d2)
        remove('test1.pkl')
        save_yaml(d, 'test1.pkl.gz')
        d2 = load_yaml('test1.pkl.gz')
        self.assertDictEqual(d, d2)
        remove('test1.pkl.gz')
        with self.assertRaises(FileNotFoundError):
            save_yaml(d, 'data/test1.pkl')
        with self.assertRaises(FileNotFoundError):
            save_yaml(d, 'data/test1.pkl.gz')
        save_yaml(d, 'data/test1.pkl', force=True)
        d2 = load_yaml('data/test1.pkl')
        self.assertDictEqual(d, d2)
        remove('data/test1.pkl')
        rmdir('data/')
        save_yaml(d, 'data/test1.pkl.gz', force=True)
        d2 = load_yaml('data/test1.pkl.gz')
        self.assertDictEqual(d, d2)
        remove('data/test1.pkl.gz')
        rmdir('data/')

    def test_copy_files_(self) -> None:
        copy_files('data/', 'mysutils/__init__.py', 'mysutils/file.py')
        self.assertListEqual([True, True], [exists('data/__init__.py'), exists('data/file.py')])
        self.assertTupleEqual(execute_command(['ls', 'data']), ('file.py\n__init__.py\n', ''))
        remove('data/__init__.py')
        remove('data/file.py')
        rmdir('data/')
        with self.assertRaises(FileNotFoundError):
            copy_files('data/', 'mysutils/__init__.py', 'mysutils/file.py', force=False)
        self.assertTupleEqual(execute_command(['ls', 'data']),
                              ('', "ls: cannot access 'data': No such file or directory\n"))



if __name__ == '__main__':
    unittest.main()

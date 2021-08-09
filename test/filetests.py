import unittest
from os import remove
from os.path import exists

from mysutils.command import execute_command
from mysutils.file import save_json, load_json, save_pickle, load_pickle, copy_files, remove_files, gzip_compress, \
    gzip_decompress, open_file, first_line
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
        remove_files('data/test1.json', 'data/')
        self.assertListEqual([False, False], [exists('data/test1.json'), exists('data/')])
        save_json(d, 'data/test1.json.gz', force=True)
        d2 = load_json('data/test1.json.gz')
        self.assertDictEqual(d, d2)
        remove_files('data/test1.json.gz', 'data/')

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
        remove_files('data/test1.pkl', 'data/')
        save_pickle(d, 'data/test1.pkl.gz', force=True)
        d2 = load_pickle('data/test1.pkl.gz')
        self.assertDictEqual(d, d2)
        remove_files('data/test1.pkl.gz', 'data/')

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
        remove_files('data/test1.pkl', 'data/')
        save_yaml(d, 'data/test1.pkl.gz', force=True)
        d2 = load_yaml('data/test1.pkl.gz')
        self.assertDictEqual(d, d2)
        remove_files('data/test1.pkl.gz', 'data/')

    def test_copy_files_(self) -> None:
        copy_files('data/', 'mysutils/__init__.py', 'mysutils/file.py')
        self.assertListEqual([True, True], [exists('data/__init__.py'), exists('data/file.py')])
        self.assertTupleEqual(execute_command(['ls', 'data']), ('file.py\n__init__.py\n', ''))
        remove_files('data/__init__.py', 'data/file.py', 'data/')
        with self.assertRaises(FileNotFoundError):
            copy_files('data/', 'mysutils/__init__.py', 'mysutils/file.py', force=False)
        self.assertTupleEqual(execute_command(['ls', 'data']),
                              ('', "ls: cannot access 'data': No such file or directory\n"))

    def test_compress_gzip(self) -> None:
        # Create a file
        d = {
            'version': 1.0,
            'file_list': ['1.txt', '2.txt']
        }
        save_json(d, 'test.json')

        # Compress the file
        gzip_compress('test.json', 'test.json.gz')
        # Decompress the file
        gzip_decompress('test.json.gz', 'test2.json')
        # Load and compare the decompress file
        d2 = load_json('test2.json')
        self.assertDictEqual(d, d2)
        with self.assertRaises(ValueError):
            gzip_compress('test.json', 'test.json')
        with self.assertRaises(ValueError):
            gzip_decompress('test.json.gz', 'test.json.gz')

        remove_files('test.json', 'test.json.gz', 'test2.json')

    def test_first_line(self) -> None:
        # Test with \n at the end
        with open_file('test/text.txt.gz', 'wt') as file:
            print('First line', file=file)
            print('Second line', file=file)
        line = first_line('test/text.txt.gz')
        self.assertEqual(line, 'First line')
        # Test empty file
        with open_file('test/text.txt.gz', 'wt'):
            pass
        line = first_line('test/text.txt.gz')
        self.assertEqual(line, '')
        # Test without \n at the end
        with open_file('test/text.txt', 'wt') as file:
            file.write('First line')
        line = first_line('test/text.txt')
        self.assertEqual(line, 'First line')
        remove_files('test/text.txt', 'test/text.txt.gz')


if __name__ == '__main__':
    unittest.main()

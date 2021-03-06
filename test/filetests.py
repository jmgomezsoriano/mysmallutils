import shutil
from os import remove, rmdir
from os.path import exists

from mysutils.command import execute_command
from mysutils import unittest
from mysutils.file import save_json, load_json, save_pickle, load_pickle, copy_files, remove_files, gzip_compress, \
    gzip_decompress, open_file, first_line, exist_files, count_lines, touch, read_file, cat, mkdirs, move_files, \
    first_file, last_file, output_file_path, list_dir, head, body, tail, last_line, read_files, read_from, read_until, \
    has_encoding
from mysutils.tmp import removable_files, removable_tmp, removable_tmps
from mysutils.yaml import load_yaml, save_yaml


def generate_example_files():
    with open_file('test1.txt', 'wt') as f:
        for i in range(10):
            print(i, file=f)
    with open_file('test2.txt.gz', 'wt') as f:
        for i in range(65, 75):
            print(chr(i), file=f)
    return ['test1.txt', 'test2.txt.gz']


def remove_example_files():
    remove_files('test1.txt', 'test2.txt.gz')


class FileTestCase(unittest.FileTestCase):
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
        with open_file('text.txt.gz', 'wt') as file:
            print('First line', file=file)
            print('Second line', file=file)
        line = first_line('text.txt.gz')
        self.assertEqual(line, 'First line')
        # Test empty file
        with open_file('text.txt.gz', 'wt'):
            pass
        line = first_line('text.txt.gz')
        self.assertEqual(line, '')
        # Test without \n at the end
        with open_file('text.txt', 'wt') as file:
            file.write('First line')
        line = first_line('text.txt')
        self.assertEqual(line, 'First line')
        remove_files('text.txt', 'text.txt.gz')

    def test_exist_files(self) -> None:
        self.assertTrue(exist_files('mysutils/collections.py', 'test/filetests.py', 'mysutils/file.py'))
        self.assertFalse(exist_files('mysutils/collections.py', 'test/filetests.py', 'test/mysutils/file.py'))
        self.assertFalse(exist_files('data/test/filetests.py', 'test/mysutils/file.py'))

    def test_count_lines(self) -> None:
        with open_file('text.txt.gz', 'wt') as file:
            print('First line', file=file)
            print('Second line', file=file)
        self.assertEqual(count_lines('text.txt.gz'), 2)
        remove_files('text.txt.gz')

    def test_touch(self) -> None:
        touch('text.txt')
        self.assertExists('text.txt')
        self.assertEqual(count_lines('text.txt'), 0)
        touch('1.txt', '2.txt', '3.txt')
        self.assertExists('1.txt', '2.txt', '3.txt')
        remove_files('text.txt', '1.txt', '2.txt', '3.txt')

    def test_read_file(self) -> None:
        with open_file('text.txt.gz', 'wt') as file:
            print('First line', file=file)
            print('Second line', file=file)
        lines = read_file('text.txt.gz')
        self.assertEqual(lines[0], 'First line\n')
        self.assertEqual(lines[1], 'Second line\n')
        self.assertEqual(len(lines), 2)
        lines = read_file('text.txt.gz', False)
        self.assertEqual(lines[0], 'First line')
        self.assertEqual(lines[1], 'Second line')
        self.assertEqual(len(lines), 2)
        with open_file('text.txt', 'wt') as file:
            print('First line', file=file)
            print('Second line', file=file)
        lines = read_file('text.txt')
        self.assertEqual(lines[0], 'First line\n')
        self.assertEqual(lines[1], 'Second line\n')
        self.assertEqual(len(lines), 2)
        lines = read_file('text.txt', False)
        self.assertEqual(lines[0], 'First line')
        self.assertEqual(lines[1], 'Second line')
        self.assertEqual(len(lines), 2)
        remove_files('text.txt.gz', 'text.txt')

    def test_cat(self) -> None:
        with open_file('text.txt.gz', 'wt') as file:
            print('First line', file=file)
            print('Second line', file=file)
        with open_file('text_cat.txt.gz', 'wt') as file:
            cat('text.txt.gz', output=file)
        lines = read_file('text_cat.txt.gz')
        self.assertEqual(lines[0], 'First line\n')
        self.assertEqual(lines[1], 'Second line\n')
        self.assertEqual(len(lines), 2)

        with open_file('text.txt', 'wt') as file:
            print('First line', file=file)
            print('Second line', file=file)
        with open_file('text_cat.txt', 'wt') as file:
            cat('text.txt', output=file)
        lines = read_file('text_cat.txt', False)
        self.assertEqual(lines[0], 'First line')
        self.assertEqual(lines[1], 'Second line')
        self.assertEqual(len(lines), 2)
        remove_files('text.txt.gz', 'text_cat.txt.gz', 'text.txt', 'text_cat.txt')

    def test_mkdir(self) -> None:
        # Create the folder if not exists
        mkdirs('new_folder')
        self.assertExists('new_folder')
        # Do nothing because the folder was already created.
        mkdirs('new_folder')
        rmdir('new_folder')

    def test_move_files(self) -> None:
        touch('1.txt', '2.txt', '3.txt')
        move_files('test/', '1.txt', '2.txt', '3.txt')
        self.assertExists('test/1.txt', 'test/2.txt', 'test/3.txt')
        self.assertNotExists('1.txt', '2.txt', '3.txt')
        with self.assertRaises(IsADirectoryError):
            move_files('test2/', 'test/1.txt', 'test/2.txt', 'test/3.txt')
        move_files('test2/', 'test/1.txt', 'test/2.txt', 'test/3.txt', force=True)
        self.assertExists('test2/1.txt', 'test2/2.txt', 'test2/3.txt')
        self.assertNotExists('test/1.txt', 'test/2.txt', 'test/3.txt')
        touch('1.txt', '2.txt', '3.txt')
        with self.assertRaises(shutil.Error):
            move_files('test2/', '1.txt', '2.txt', '3.txt')
        move_files('test2/', '1.txt', '2.txt', '3.txt', replace=True)
        remove_files('test2/1.txt', 'test2/2.txt', 'test2/3.txt', 'test2')

    def test_first_and_last(self) -> None:
        touch('1.txt', '2.txt', '3.txt', 'x.out', 'y.out', 'z.out')
        self.assertExists('1.txt', '2.txt', '3.txt', 'x.out', 'y.out', 'z.out')
        self.assertEqual(first_file(), './.git')
        self.assertEqual(first_file('test'), 'test/__init__.py')
        self.assertEqual(first_file('.', r'.*\.txt$'), './1.txt')
        self.assertEqual(first_file('.', r'.*\.out$'), './x.out')
        self.assertEqual(last_file(), './z.out')
        self.assertEqual(last_file('test'), 'test/webtests.py')
        self.assertEqual(last_file('.', r'.*\.txt$'), './requirements.txt')
        self.assertEqual(last_file('.', r'.*\.out$'), './z.out')
        remove_files('1.txt', '2.txt', '3.txt', 'x.out', 'y.out', 'z.out')

    def test_output_file_path(self) -> None:
        self.assertRegex(output_file_path(), r'^./[0-9]{8}-[0-9]{6}$')
        self.assertRegex(output_file_path('model'), r'^model/[0-9]{8}-[0-9]{6}$')
        self.assertRegex(output_file_path('model', '.tar.gz'), r'^model/[0-9]{8}-[0-9]{6}.tar.gz$')
        self.assertRegex(
            output_file_path('model', '.tar.gz', True, method='svm', k=0.7, passes=300, lemma=True, stopw=False),
            r'^model/[0-9]{8}-[0-9]{6}-svm-0.7-300-lemma.tar.gz$')
        self.assertEqual(
            output_file_path('model', '.tar.gz', False, method='svm', k=0.7, passes=300, lemma=True, stopw=False),
            'model/svm-0.7-300-lemma.tar.gz')
        self.assertEqual(
            output_file_path('model', '.tar.gz', False, method=None, k=0.7, passes='', lemma=False, stopw=True),
            'model/0.7-stopw.tar.gz'
        )

    def test_list_folder(self) -> None:
        mkdirs('data')
        touch('data/1.txt', 'data/2.txt', 'data/3.out')
        self.assertListEqual(list_dir('data'), ['data/1.txt', 'data/2.txt', 'data/3.out'])
        self.assertListEqual(list_dir('data', r'.*\.out$'), ['data/3.out'])
        remove_files('data', recursive=True)

    def test_head(self) -> None:
        self.assertListEqual(head('README.md', 2), ['# MySmallUtils', 'Small Python utils to do life easier.'])
        self.assertLess(len(head('README.md', 100000)), 100000)

    def test_body(self) -> None:
        self.assertListEqual(body('README.md', 0, 2), ['# MySmallUtils', 'Small Python utils to do life easier.'])
        self.assertListEqual(body('README.md', 2, 2),
                             ['', 'This includes tools to execute external commands, compress files,'])

    def test_tail(self) -> None:
        self.assertListEqual(tail('README.md', 100000)[:2],
                             ['# MySmallUtils', 'Small Python utils to do life easier.'])
        self.assertListEqual(tail('README.md', 3),
                             ['# How to collaborate',
                              '',
                              'I you want to collaborate with this project, please, '
                              '<a href="mailto:jmgomez.soriano@gmail.com">contact with me</a>.'])
        self.assertEqual(last_line('README.md'),
                         'I you want to collaborate with this project, please, '
                         '<a href="mailto:jmgomez.soriano@gmail.com">contact with me</a>.')

    def test_read_files(self) -> None:
        n1, n2 = count_lines('README.md'), count_lines('requirements.txt')
        self.assertEqual(count_lines('requirements.txt', 'README.md'), n1 + n2)
        self.assertEqual(len(read_files('requirements.txt', 'README.md')), n1 + n2)

    def test_read_from(self) -> None:
        with removable_files(*generate_example_files()):
            lines = read_from('test1.txt')
            self.assertEqual(len(lines), 10)
            lines = read_until('test1.txt')
            self.assertEqual(len(lines), 10)
            lines = read_from('test1.txt', '5')
            self.assertEqual(len(lines), 5)
            lines = read_until('test1.txt', '5')
            self.assertEqual(len(lines), 5)
            lines = read_from('test2.txt.gz')
            self.assertEqual(len(lines), 10)
            lines = read_until('test2.txt.gz')
            self.assertEqual(len(lines), 10)
            lines = read_from('test2.txt.gz', 'F')
            self.assertEqual(len(lines), 5)
            lines = read_until('test2.txt.gz', 'F')
            self.assertEqual(len(lines), 5)
            lines = read_from('test1.txt', '10')
            self.assertEqual(len(lines), 0)
            lines = read_until('test2.txt.gz', 'f')
            self.assertEqual(len(lines), 10)
            lines = read_from('test2.txt.gz', '^f', True)
            self.assertEqual(len(lines), 5)
            lines = read_until('test2.txt.gz', '^f', True)
            self.assertEqual(len(lines), 5)

    def test_encoding(self) -> None:
        with removable_tmp() as tmp:
            with open_file(tmp, 'wt', encoding='iso8859-1') as file:
                file.write('??Es una ca??a at??mica!')
            self.assertTrue(has_encoding(tmp, 'iso8859-1'))
            self.assertFalse(has_encoding(tmp, 'utf-8'))
            self.assertEncoding(tmp, encoding='iso8859-1')
            self.assertNotEncoding(tmp, encoding='utf-8')
        with removable_tmp(suffix='.gz') as tmp:
            with open_file(tmp, 'wt', encoding='iso8859-1') as file:
                file.write('??Es una ca??a at??mica!')
            self.assertTrue(has_encoding(tmp, 'iso8859-1'))
            self.assertFalse(has_encoding(tmp, 'utf-8'))
            self.assertEncoding(tmp, encoding='iso8859-1')
            self.assertNotEncoding(tmp, encoding='utf-8')
        d = {'name': 'Mar??a G??mez', 'message': '??Es una ca??a at??mica!'}
        with removable_tmps(2) as (json_tmp, yaml_tmp):
            save_json(d, json_tmp, encoding='iso8859-1')
            save_yaml(d, yaml_tmp, encoding='iso8859-1')
            self.assertEncoding(json_tmp, yaml_tmp, encoding='iso8859-1')
            self.assertNotEncoding(json_tmp, yaml_tmp, encoding='utf-8')
            self.assertDictEqual(d, load_json(json_tmp, 'iso8859-1'))
            self.assertDictEqual(d, load_yaml(yaml_tmp, 'iso8859-1'))
            with self.assertRaises(FileNotFoundError):
                self.assertDictEqual(d, load_json(json_tmp + '.json'))
            with self.assertRaises(FileNotFoundError):
                self.assertDictEqual(d, load_yaml(yaml_tmp + '.yaml'))

    def test_defaults(self) -> None:
        d = {'name': 'John Smith', 'message': 'Hello world!'}
        with removable_tmps(3) as (json_tmp, yaml_tmp, pickle_tmp):
            save_json(d, json_tmp)
            save_yaml(d, yaml_tmp)
            save_pickle(d, pickle_tmp)
            self.assertDictEqual(d, load_json(json_tmp, default={}))
            self.assertDictEqual(d, load_yaml(yaml_tmp, default={}))
            self.assertDictEqual(d, load_pickle(pickle_tmp, default={}))
            self.assertDictEqual({}, load_json(json_tmp + '.json', default={}))
            self.assertDictEqual({}, load_yaml(yaml_tmp + '.yaml', default={}))
            self.assertDictEqual({}, load_pickle(pickle_tmp + '.pkl', default={}))
            default={'name': 'Anybody', 'message': 'None'}
            self.assertDictEqual(default, load_json(json_tmp + '.json', default=default))
            self.assertDictEqual(default, load_yaml(yaml_tmp + '.yaml', default=default))
            self.assertDictEqual(default, load_pickle(pickle_tmp + '.pkl', default=default))


if __name__ == '__main__':
    unittest.main()

import shutil
from os import remove, rmdir, mkdir
from os.path import exists, join

from mysutils import unittest
from mysutils.file import save_json, load_json, save_pickle, load_pickle, copy_files, remove_files, gzip_compress, \
    gzip_decompress, open_file, first_line, exist_files, count_lines, touch, read_file, cat, mkdirs, move_files, \
    first_file, last_file, output_file_path, list_dir, head, body, tail, last_line, read_files, read_from, read_until, \
    has_encoding, write_file, expand_wildcards, to_filename
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
        with removable_tmp(True) as tmp:
            save_json(d, join(tmp, 'test1.json'))
            d2 = load_json(join(tmp, 'test1.json'))
            self.assertDictEqual(d, d2)
            remove(join(tmp, 'test1.json'))
            save_json(d, join(tmp, 'test1.json.gz'))
            d2 = load_json(join(tmp, 'test1.json.gz'))
            self.assertDictEqual(d, d2)
            remove(join(tmp, 'test1.json.gz'))
            with self.assertRaises(FileNotFoundError):
                save_json(d, join(tmp, 'data', 'test1.json'))
            with self.assertRaises(FileNotFoundError):
                save_json(d, join(tmp, 'data', 'test1.json.gz'))
            save_json(d, join(tmp, 'data', 'test1.json'), force=True)
            d2 = load_json(join(tmp, 'data', 'test1.json'))
            self.assertDictEqual(d, d2)
            remove_files(join(tmp, 'data', 'test1.json'), join(tmp, 'data'))
            self.assertListEqual([False, False], [exists(join(tmp, 'data', 'test1.json')), exists(join(tmp, 'data'))])
            save_json(d, join(tmp, 'data', 'test1.json.gz'), force=True)
            d2 = load_json(join(tmp, 'data', 'test1.json.gz'))
            self.assertDictEqual(d, d2)
            remove_files(join(tmp, 'data', 'test1.json.gz'), join(tmp, 'data'))

    def test_pickle(self) -> None:
        d = {
            'version': 1.0,
            'file_list': ['1.txt', '2.txt']
        }
        with removable_tmp(True) as tmp:
            save_pickle(d, join(tmp, 'test1.pkl'))
            d2 = load_pickle(join(tmp, 'test1.pkl'))
            self.assertDictEqual(d, d2)
            remove(join(tmp, 'test1.pkl'))
            save_pickle(d, join(tmp, 'test1.pkl.gz'))
            d2 = load_pickle(join(tmp, 'test1.pkl.gz'))
            self.assertDictEqual(d, d2)
            remove(join(tmp, 'test1.pkl.gz'))
            with self.assertRaises(FileNotFoundError):
                save_pickle(d, join(tmp, 'data', 'test1.pkl'))
            with self.assertRaises(FileNotFoundError):
                save_pickle(d, join(tmp, 'data', 'test1.pkl.gz'))
            save_pickle(d, join(tmp, 'data', 'test1.pkl'), force=True)
            d2 = load_pickle(join(tmp, 'data', 'test1.pkl'))
            self.assertDictEqual(d, d2)
            remove_files(join(tmp, 'data', 'test1.pkl'), join(tmp, 'data'))
            save_pickle(d, join(tmp, 'data', 'test1.pkl.gz'), force=True)
            d2 = load_pickle(join(tmp, 'data', 'test1.pkl.gz'))
            self.assertDictEqual(d, d2)
            remove_files(join(tmp, 'data', 'test1.pkl.gz'), join(tmp, 'data'))

    def test_yaml(self) -> None:
        d = {
            'version': 1.0,
            'file_list': ['1.txt', '2.txt']
        }
        with removable_tmp(True) as tmp:
            save_yaml(d, join(tmp, 'test1.pkl'))
            d2 = load_yaml(join(tmp, 'test1.pkl'))
            self.assertDictEqual(d, d2)
            remove(join(tmp, 'test1.pkl'))
            save_yaml(d, join(tmp, 'test1.pkl.gz'))
            d2 = load_yaml(join(tmp, 'test1.pkl.gz'))
            self.assertDictEqual(d, d2)
            remove(join(tmp, 'test1.pkl.gz'))
            with self.assertRaises(FileNotFoundError):
                save_yaml(d, join(tmp, 'data', 'test1.pkl'))
            with self.assertRaises(FileNotFoundError):
                save_yaml(d, join(tmp, 'data', 'test1.pkl.gz'))
            save_yaml(d, join(tmp, 'data', 'test1.pkl'), force=True)
            d2 = load_yaml(join(tmp, 'data', 'test1.pkl'))
            self.assertDictEqual(d, d2)
            remove_files(join(tmp, 'data', 'test1.pkl'), join(tmp, 'data'))
            save_yaml(d, join(tmp, 'data', 'test1.pkl.gz'), force=True)
            d2 = load_yaml(join(tmp, 'data', 'test1.pkl.gz'))
            self.assertDictEqual(d, d2)

    def test_copy_files(self) -> None:
        with removable_tmp(True) as tmp:
            touch(join(tmp, 'test1.txt'), join(tmp, 'test2.txt'))
            mkdir(join(tmp, 'data'))
            copy_files(join(tmp, 'data'), join(tmp, 'test1.txt'), join(tmp, 'test2.txt'))
            self.assertListEqual([True, True], [exists(join(tmp, 'test1.txt')), exists(join(tmp, 'test2.txt'))])
            self.assertListEqual([True, True],
                                 [exists(join(tmp, 'data', 'test1.txt')), exists(join(tmp, 'data', 'test2.txt'))])
            self.assertListEqual([f.rsplit('\\', 1)[1] for f in list_dir(tmp)], ['data', 'test1.txt', 'test2.txt'])
            remove_files(join(tmp, 'test1.txt'), join(tmp, 'test2.txt'), join(tmp, 'data/'), recursive=True)
            self.assertListEqual([False] * 3, [exists(join(tmp, f)) for f in ['test1.txt', 'test2.txt', 'data']])
            touch(join(tmp, 'test1.txt'), join(tmp, 'test2.txt'))
            with removable_tmp(True) as tmp2:
                with self.assertRaises(FileNotFoundError):
                    copy_files(join(tmp2, 'data'), join(tmp, 'test1.txt'), join(tmp, 'test2.txt'), force=False)
                self.assertListEqual(list_dir(tmp2), [])
                copy_files(join(tmp2, 'data'), join(tmp, 'test1.txt'), join(tmp, 'test2.txt'))
                self.assertExists(*[join(tmp2, 'data', f) for f in ['test1.txt', 'test2.txt']])

    def test_move_files(self) -> None:
        with removable_tmp(True) as tmp:
            files = [join(tmp, f) for f in ['1.txt', '2.txt', '3.txt']]
            files_test = [join(tmp, 'test', f) for f in ['1.txt', '2.txt', '3.txt']]
            files_test2 = [join(tmp, 'test2', f) for f in ['1.txt', '2.txt', '3.txt']]
            touch(*files)
            mkdirs(join(tmp, 'test'))
            move_files(join(tmp, 'test'), *files)
            self.assertExists(*files_test)
            self.assertNotExists(*files)
            with self.assertRaises(FileNotFoundError):
                move_files(join(tmp, 'test2'), *files_test)
            move_files(join(tmp, 'test2'), *files_test, force=True)
            self.assertExists(*files_test2)
            self.assertNotExists(*files_test)
            touch(*files)
            with self.assertRaises(NotADirectoryError):
                move_files(join(tmp, 'test2', '1.txt'), *files)
            with self.assertRaises(shutil.Error):
                move_files(join(tmp, 'test2'), *files)
            move_files(join(tmp, 'test2'), *files, replace=True)

    def test_remove_files(self) -> None:
        with removable_tmp(True) as tmp:
            files = [join(tmp, f) for f in ['1.txt', '2.txt', '3.json', '4.yaml']]
            touch(*files)
            self.assertExists(*files)
            remove_files(*files)
            self.assertNotExists(*files)
            touch(*files)
            remove_files(join(tmp, '*.txt'), join(tmp, '*.yaml'))
            self.assertExists(join(tmp, '3.json'))
            files = [join(tmp, 'data', f) for f in ['1.txt', '2.txt', '3.json', '4.yaml']]
            mkdirs(join(tmp, 'data'))
            touch(*files)
            with self.assertRaises(OSError):
                remove_files(join(tmp, 'data'))
            self.assertExists(*files)
            remove_files(join(tmp, 'data'), recursive=True)
            self.assertNotExists(join(tmp, 'data'))

    def test_expanding_wildcards(self) -> None:
        with removable_tmp(True) as tmp:
            files = [join(tmp, f) for f in ['1.txt', '2.txt', '3.json', '4.yaml']]
            touch(*files)
            self.assertListEqual(expand_wildcards(join(tmp, '*.txt'), join(tmp, '*.yaml')),
                                 [files[0], files[1], files[3]])

    def test_copy_files_wildcards(self) -> None:
        with removable_tmp(True) as tmp:
            files = join(tmp, 'test1.txt'), join(tmp, 'test2.txt'), join(tmp, 'test3.json'), join(tmp, 'test4.yaml')
            touch(*files)
            mkdir(join(tmp, 'data'))
            copy_files(join(tmp, 'data'), join(tmp, '*.txt'), join(tmp, '*.yaml'))
            data_tmp = join(tmp, 'data')
            self.assertExists(join(data_tmp, 'test1.txt'), join(data_tmp, 'test2.txt'), join(data_tmp, 'test4.yaml'))
            self.assertNotExists(join(data_tmp, 'test3.json'))
            self.assertExists(*files)

    def test_move_files_wildcards(self) -> None:
        with removable_tmp(True) as tmp:
            files = [join(tmp, f) for f in ['1.txt', '2.txt', '3.json', '4.yaml']]
            touch(*files)
            mkdirs(join(tmp, 'data'))
            move_files(join(tmp, 'data'), join(tmp, '*.txt'), join(tmp, '*.yaml'))
            self.assertExists(join(tmp, 'data', '1.txt'), join(tmp, 'data', '2.txt'), join(tmp, 'data', '4.yaml'))
            self.assertNotExists(join(tmp, 'data', 'test3.json'))
            self.assertNotExists(join(tmp, '1.txt'), join(tmp, '2.txt'), join(tmp, '4.yaml'))
            self.assertExists(join(tmp, '3.json'))

    def test_compress_gzip(self) -> None:
        # Create a file
        d = {
            'version': 1.0,
            'file_list': ['1.txt', '2.txt']
        }
        with removable_tmp(True) as tmp:
            save_json(d, join(tmp, 'test.json'))
            # Compress the file
            gzip_compress(join(tmp, 'test.json'), join(tmp, 'test.json.gz'))
            # Decompress the file
            gzip_decompress(join(tmp, 'test.json.gz'), join(tmp, 'test2.json'))
            # Load and compare the decompress file
            d2 = load_json(join(tmp, 'test2.json'))
            self.assertDictEqual(d, d2)
            with self.assertRaises(ValueError):
                gzip_compress(join(tmp, 'test.json'), join(tmp, 'test.json'))
            with self.assertRaises(ValueError):
                gzip_decompress(join(tmp, 'test.json.gz'), join(tmp, 'test.json.gz'))

    def test_first_line(self) -> None:
        with removable_tmp(True) as tmp:
            # Test with \n at the end
            with open_file(join(tmp, 'text.txt.gz'), 'wt') as file:
                print('First line', file=file)
                print('Second line', file=file)
            line = first_line(join(tmp, 'text.txt.gz'))
            self.assertEqual(line, 'First line')
            # Test empty file
            with open_file(join(tmp, 'text.txt.gz'), 'wt'):
                pass
            line = first_line(join(tmp, 'text.txt.gz'))
            self.assertEqual(line, '')
            # Test without \n at the end
            with open_file(join(tmp, 'text.txt'), 'wt') as file:
                file.write('First line')
            line = first_line(join(tmp, 'text.txt'))
            self.assertEqual(line, 'First line')

    def test_exist_files(self) -> None:
        self.assertTrue(exist_files('mysutils/collections.py', 'test/filetests.py', 'mysutils/file.py'))
        self.assertFalse(exist_files('mysutils/collections.py', 'test/filetests.py', 'test/mysutils/file.py'))
        self.assertFalse(exist_files('data/test/filetests.py', 'test/mysutils/file.py'))

    def test_count_lines(self) -> None:
        with removable_tmp(suffix='.gz') as tmp:
            with open_file(tmp, 'wt') as file:
                print('First line', file=file)
                print('Second line', file=file)
            self.assertEqual(count_lines(tmp), 2)

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

    def test_write_file(self) -> None:
        write_file('text.txt', 'This is an example of writing text in a file.')
        self.assertEqual(first_line('text.txt'), 'This is an example of writing text in a file.')
        # Write a text in a compressed file
        write_file('text.txt.gz', 'This is an example of writing text in a file.')
        self.assertEqual(first_line('text.txt.gz'), 'This is an example of writing text in a file.')
        text = ['This is another exmaple of writing text in a file.', 'This file has several lines.']
        write_file('text.txt', text)
        self.assertEqual(read_file('text.txt', False), text)
        write_file('text.txt.gz', text)
        self.assertEqual(read_file('text.txt.gz', False), text)
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

    def test_first_and_last(self) -> None:
        with removable_tmp(True) as tmp:
            files = [join(tmp, f) for f in ['1.txt', '2.txt', '3.txt', 'x.out', 'y.out', 'z.out']]
            touch(*files)
            self.assertExists(*files)
            self.assertIn('1.txt', first_file(tmp), True)
            self.assertEqual(first_file(tmp, r'.*\.txt$'), join(tmp, '1.txt'))
            self.assertEqual(first_file(tmp, r'.*\.out$'), join(tmp, 'x.out'))
            self.assertEqual(last_file(tmp), join(tmp, 'z.out'))
            self.assertEqual(last_file(tmp, r'.*\.txt$'), join(tmp, '3.txt'))
            self.assertEqual(last_file(tmp, r'.*\.out$'), join(tmp, 'z.out'))

    def test_output_file_path(self) -> None:
        self.assertRegex(output_file_path(), r'^.(/|\\)[0-9]{8}-[0-9]{6}$')
        self.assertRegex(output_file_path('model'), r'^model(/|\\)[0-9]{8}-[0-9]{6}$')
        self.assertRegex(output_file_path('model', '.tar.gz'), r'^model(/|\\)[0-9]{8}-[0-9]{6}.tar.gz$')
        self.assertRegex(
            output_file_path('model', '.tar.gz', True, method='svm', k=0.7, passes=300, lemma=True, stopw=False),
            r'^model(/|\\)[0-9]{8}-[0-9]{6}-svm-0.7-300-lemma.tar.gz$')
        self.assertRegex(
            output_file_path('model', '.tar.gz', False, method='svm', k=0.7, passes=300, lemma=True, stopw=False),
            r'model(/|\\)svm-0.7-300-lemma.tar.gz')
        self.assertRegex(
            output_file_path('model', '.tar.gz', False, method=None, k=0.7, passes='', lemma=False, stopw=True),
            r'model(/|\\)0.7-stopw.tar.gz'
        )

    def test_list_folder(self) -> None:
        with removable_tmp(True) as tmp:
            mkdirs(join(tmp, 'data'))
            touch(*[join(tmp, 'data', f) for f in ['1.txt', '2.txt', '3.out']])
            self.assertListEqual(list_dir(join(tmp, 'data')), [join(tmp, 'data', f) for f in ['1.txt', '2.txt', '3.out']])
            self.assertListEqual(list_dir(join(tmp, 'data'), r'.*\.out$'), [join(tmp, 'data', '3.out')])
            remove_files(join(tmp, 'data'), recursive=True)

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
                file.write('¡Es una caña atómica!')
            self.assertTrue(has_encoding(tmp, 'iso8859-1'))
            self.assertFalse(has_encoding(tmp, 'utf-8'))
            self.assertEncoding(tmp, encoding='iso8859-1')
            self.assertNotEncoding(tmp, encoding='utf-8')
        with removable_tmp(suffix='.gz') as tmp:
            with open_file(tmp, 'wt', encoding='iso8859-1') as file:
                file.write('¡Es una caña atómica!')
            self.assertTrue(has_encoding(tmp, 'iso8859-1'))
            self.assertFalse(has_encoding(tmp, 'utf-8'))
            self.assertEncoding(tmp, encoding='iso8859-1')
            self.assertNotEncoding(tmp, encoding='utf-8')
        d = {'name': 'María Gómez', 'message': '¡Es una caña atómica!'}
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

    def test_to_filename(self) -> None:
        self.assertEqual(to_filename('Hello World! How are you?'), "Hello World_ How are you_")
        self.assertEqual(to_filename('Hello World! How are you?', '.srt'), "Hello World_ How are you_.srt")

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

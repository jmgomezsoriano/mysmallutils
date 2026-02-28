import json
import shutil
from mysutils import unittest
from os import mkdir
from os.path import exists, join

from mysutils.file import save_json, remove_files, exist_files, load_json, mkdirs, touch
from mysutils.tar import create_tar, detect_compress_method, list_tar, extract_tar_file, open_tar_file, load_tar_json, \
    extract_tar_files, extract_tar, add_tar_files, add_compressed_tar_files, exist_tar_files
from mysutils.tmp import removable_files


def create_files() -> dict:
    d = {
        'version': 1.0,
        'file_list': ['1.txt', '2.txt']
    }
    save_json(d, 'test.json')
    save_json(d, 'test.json.gz')
    return d


def create_tar_files() -> None:
    if exists('data/'):
        shutil.rmtree('data')
    create_tar('test.tar.gz', 'test.json', 'test.json.gz')
    create_tar('test.tar.bz2', 'test.json', 'test.json.gz')
    create_tar('test.tar.xz', 'test.json', 'test.json.gz')
    create_tar('test.tar', 'test.json', 'test.json.gz')


class MyTestCase(unittest.FileTestCase):
    @staticmethod
    def remove_files() -> None:
        remove_files('test.tar.gz', 'test.tar.bz2', 'test.tar.xz', 'test.tar', 'test.json', 'test.json.gz',
                     ignore_errors=True)

    def test_create_tar_files(self) -> None:
        if exists('data/'):
            shutil.rmtree('data')
        with self.assertRaises(FileNotFoundError):
            create_tar('test2/test2.tar.gz', 'test.json', 'test.json.gz')
        create_files()
        create_tar_files()
        exist_files('test.tar.gz', 'test.tar.bz2', 'test.tar.xz', 'test.tar')
        self.remove_files()

    def test_detect_method(self) -> None:
        self.assertEqual('gz', detect_compress_method('test.tar.gz'))
        self.assertEqual('bz2', detect_compress_method('test.tar.bz2'))
        self.assertEqual('xz', detect_compress_method('test.tar.xz'))
        self.assertEqual('', detect_compress_method('test.tar'))

    def test_list_tar_files(self) -> None:
        create_files()
        create_tar_files()
        lst = list_tar('test.tar.gz')
        self.assertEqual(len(lst), 2)
        self.assertEqual(lst[0].path, 'test.json')
        self.assertEqual(lst[1].path, 'test.json.gz')
        self.remove_files()

    def test_extract_file(self) -> None:
        d = create_files()
        create_tar_files()
        extract_tar_file('test.tar.gz', 'test2.json', 'test.json')
        self.assertExists('test2.json')
        d2 = load_json('test2.json')
        self.assertDictEqual(d, d2)
        remove_files('test2.json')
        self.remove_files()

    def test_extract_file_in_folder(self) -> None:
        d = create_files()
        create_tar_files()
        mkdir('data')
        extract_tar_file('test.tar.gz', 'data/', 'test.json')
        self.assertExists('data/test.json')
        d2 = load_json('data/test.json')
        self.assertDictEqual(d, d2)
        remove_files('data/test.json', 'data')
        self.remove_files()

    def test_open_tar_file(self) -> None:
        d = create_files()
        create_tar_files()
        with open_tar_file('test.tar.gz', 'test.json') as file:
            d2 = json.load(file)
            self.assertDictEqual(d, d2)
        self.remove_files()

    def test_load_json_from_tar(self) -> None:
        d = create_files()
        create_tar_files()
        d2 = load_tar_json('test.tar.gz', 'test.json.gz')
        self.assertDictEqual(d, d2)
        d2 = load_tar_json('test.tar.gz', 'test.json')
        self.assertDictEqual(d, d2)
        self.remove_files()

    def test_force_extract(self) -> None:
        create_files()
        create_tar_files()
        with self.assertRaises(ValueError):
            extract_tar_files('test.tar.bz2', 'data')
        extract_tar_files('test.tar.bz2', 'data/', 'test.json', 'test.json.gz', force=True)
        extract_tar_files('test.tar.bz2', 'data/', 'test.json', 'test.json.gz', verbose=True)
        self.assertExists('data', 'data/test.json', 'data/test.json.gz')
        remove_files('data/test.json', 'data/test.json.gz', 'data')
        extract_tar_files('test.tar.bz2', 'data', force=True)
        self.assertExists('data/test.json', 'data/test.json.gz')
        remove_files('data/test.json', 'data/test.json.gz', 'data')
        self.remove_files()

    def test_extract_tar(self) -> None:
        create_files()
        create_tar_files()
        # Check error when the folder does not exist
        with self.assertRaises(FileNotFoundError):
            extract_tar('test/test.tar', 'data')
        # Force the folder creation
        extract_tar('test.tar', 'data/', True)
        self.assertExists('data/test.json', 'data/test.json.gz')
        remove_files('data/test.json', 'data/test.json.gz')
        # Check without folder creation
        extract_tar('test.tar', 'data/', False)
        self.assertExists('data/test.json', 'data/test.json.gz')
        remove_files('data/test.json', 'data/test.json.gz')
        # Check the verbose mode
        extract_tar('test.tar', 'data/', False, True)
        self.assertExists('data/test.json', 'data/test.json.gz')
        remove_files('data/test.json', 'data/test.json.gz', 'data')

    def test_add_files(self) -> None:
        d = create_files()
        with removable_files('test.json', 'test.json.gz'):
            with removable_files(create_tar('test.tar', 'test.json.gz')) as (file,):
                add_tar_files(file, 'test.json', verbose=True)
                self.assertDictEqual(d, load_tar_json(file, 'test.json.gz'))
                self.assertDictEqual(d, load_tar_json(file, 'test.json'))
            with removable_files(create_tar('test.tar.xz', 'test.json.gz')) as (file,):
                add_tar_files(file, 'test.json')
                self.assertDictEqual(d, load_tar_json(file, 'test.json.gz'))
                self.assertDictEqual(d, load_tar_json(file, 'test.json'))
            with removable_files(create_tar('test.tar.gz', 'test.json')) as (file,):
                add_tar_files(file, 'test.json.gz')
                self.assertDictEqual(d, load_tar_json(file, 'test.json.gz'))
                self.assertDictEqual(d, load_tar_json(file, 'test.json'))
            with removable_files(create_tar('test.tar.bz2', 'test.json', verbose=True)) as (file,):
                add_tar_files(file, 'test.json.gz')
                self.assertDictEqual(d, load_tar_json(file, 'test.json.gz'))
                self.assertDictEqual(d, load_tar_json(file, 'test.json'))
            with removable_files(create_tar('test.tar.bz2')) as (file,):
                add_tar_files(file, 'test.json.gz', 'test.json')
                self.assertDictEqual(d, load_tar_json(file, 'test.json.gz'))
                self.assertDictEqual(d, load_tar_json(file, 'test.json'))
            with removable_files(add_tar_files('test.tar.gz', 'test.json.gz', 'test.json')) as (file,):
                self.assertDictEqual(d, load_tar_json(file, 'test.json.gz'))
                self.assertDictEqual(d, load_tar_json(file, 'test.json'))
            with removable_files(create_tar('test.tar')) as (file,):
                add_compressed_tar_files('test.tar', 'test.json.gz', 'test.json', compress_method='gz')
                self.assertDictEqual(d, load_tar_json(file, 'test.json.gz', compress_method='gz'))
                self.assertDictEqual(d, load_tar_json(file, 'test.json', compress_method='gz'))

    def test_exist_tar_files(self) -> None:
        with removable_files(*mkdirs('data'), recursive=True) as (folder,):
            with removable_files('test.json', 'test.json.gz'):
                create_files()
                touch(join(folder, '1.txt'), join(folder, '2.txt'), join(folder, '3.txt'))
                with removable_files('test.tar', 'test.tar.gz') as files:
                    for file in files:
                        create_tar(file, 'test.json', 'test.json.gz', 'data')
                        self.assertTrue(exist_tar_files(file, 'test.json', 'test.json.gz',
                                                        f'{folder}/1.txt', f'{folder}/2.txt', f'{folder}/3.txt'))
                        self.assertFalse(exist_tar_files(file, 'test.json', 'test.json.gz',
                                                         f'{folder}/1.txt', f'{folder}/2.txt', f'{folder}/4.txt'))


if __name__ == '__main__':
    unittest.main()

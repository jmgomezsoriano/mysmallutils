import json
import shutil
import unittest
from os import mkdir
from os.path import exists

from mysutils.file import save_json, remove_files, exist_files, load_json
from mysutils.tar import create_tar, detect_compress_method, list_tar, extract_tar_file, open_tar_file, load_tar_json, \
    extract_tar_files


def create_files() -> dict:
    d = {
        'version': 1.0,
        'file_list': ['1.txt', '2.txt']
    }
    save_json(d, 'test/test.json')
    save_json(d, 'test/test.json.gz')
    return d


def create_tar_files() -> None:
    if exists('data/'):
        shutil.rmtree('data')
    create_tar('test/test.tar.gz', 'test/test.json', 'test/test.json.gz')
    create_tar('test/test.tar.bz2', 'test/test.json', 'test/test.json.gz')
    create_tar('test/test.tar.xz', 'test/test.json', 'test/test.json.gz')
    create_tar('test/test.tar', 'test/test.json', 'test/test.json.gz')


class MyTestCase(unittest.TestCase):
    @staticmethod
    def remove_files() -> None:
        remove_files('test/test.tar.gz', 'test/test.tar.bz2', 'test/test.tar.xz', 'test/test.tar',
                     'test/test.json', 'test/test.json.gz', ignore_errors=True)

    def test_create_tar_files(self) -> None:
        if exists('data/'):
            shutil.rmtree('data')
        with self.assertRaises(FileNotFoundError):
            create_tar('tes2t/test.tar.gz', 'test/test.json', 'test/test.json.gz')
        create_files()
        create_tar_files()
        exist_files('test/test.tar.gz', 'test/test.tar.bz2', 'test/test.tar.xz', 'test/test.tar')
        self.remove_files()

    def test_detect_method(self) -> None:
        self.assertEqual('gz', detect_compress_method('test/test.tar.gz'))
        self.assertEqual('bz2', detect_compress_method('test/test.tar.bz2'))
        self.assertEqual('xz', detect_compress_method('test/test.tar.xz'))
        self.assertEqual('', detect_compress_method('test/test.tar'))

    def test_list_tar_files(self) -> None:
        create_files()
        create_tar_files()
        lst = list_tar('test/test.tar.gz')
        self.assertEqual(len(lst), 2)
        self.assertEqual(lst[0].path, 'test.json')
        self.assertEqual(lst[1].path, 'test.json.gz')
        self.remove_files()

    def test_extract_file(self) -> None:
        d = create_files()
        create_tar_files()
        extract_tar_file('test/test.tar.gz', 'test/test2.json', 'test.json')
        self.assertExists('test/test2.json')
        d2 = load_json('test/test2.json')
        self.assertDictEqual(d, d2)
        remove_files('test/test2.json')
        self.remove_files()

    def test_extract_file_in_folder(self) -> None:
        d = create_files()
        create_tar_files()
        mkdir('data')
        extract_tar_file('test/test.tar.gz', 'data/', 'test.json')
        self.assertExists('data/test.json')
        d2 = load_json('data/test.json')
        self.assertDictEqual(d, d2)
        remove_files('data/test.json', 'data')
        self.remove_files()

    def test_open_tar_file(self) -> None:
        d = create_files()
        create_tar_files()
        with open_tar_file('test/test.tar.gz', 'test.json') as file:
            d2 = json.load(file)
            self.assertDictEqual(d, d2)
        self.remove_files()

    def test_load_json_from_tar(self) -> None:
        d = create_files()
        create_tar_files()
        d2 = load_tar_json('test/test.tar.gz', 'test.json.gz')
        self.assertDictEqual(d, d2)
        d2 = load_tar_json('test/test.tar.gz', 'test.json')
        self.assertDictEqual(d, d2)
        self.remove_files()

    def test_force_extract(self) -> None:
        create_files()
        create_tar_files()
        with self.assertRaises(ValueError):
            extract_tar_files('test/test.tar.bz2', 'data')
        extract_tar_files('test/test.tar.bz2', 'data', 'test.json', 'test.json.gz', force=True)
        self.assertExists('data', 'data/test.json', 'data/test.json.gz')
        remove_files('data/test.json', 'data/test.json.gz', 'data')
        extract_tar_files('test/test.tar.bz2', 'data', force=True)
        self.assertExists('data/test.json', 'data/test.json.gz')
        remove_files('data/test.json', 'data/test.json.gz', 'data')
        self.remove_files()

    def assertExists(self, *files: str) -> None:
        self.assertTrue(exist_files(*files))


if __name__ == '__main__':
    unittest.main()

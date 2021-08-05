import json
import unittest
from os import mkdir
from os.path import exists

from mysutils.file import save_json, remove_files
from mysutils.tar import create_tar, detect_compress_method, list_tar, extract_tar_file, open_tar_file, open_tar_json


class MyTestCase(unittest.TestCase):
    def test_tar(self) -> None:
        d = {
            'version': 1.0,
            'file_list': ['1.txt', '2.txt']
        }
        save_json(d, 'test/test.json')
        save_json(d, 'test/test.json.gz')
        with self.assertRaises(FileNotFoundError):
            create_tar('tes2t/test.tar.gz', 'test/test.json', 'test/test.json.gz')
        create_tar('test/test.tar.gz', 'test/test.json', 'test/test.json.gz')
        create_tar('test/test.tar.bz2', 'test/test.json', 'test/test.json.gz')
        create_tar('test/test.tar.xz', 'test/test.json', 'test/test.json.gz')
        create_tar('test/test.tar', 'test/test.json', 'test/test.json.gz')
        self.assertEqual('gz', detect_compress_method('test/test.tar.gz'))
        self.assertEqual('bz2', detect_compress_method('test/test.tar.bz2'))
        self.assertEqual('xz', detect_compress_method('test/test.tar.xz'))
        self.assertEqual('', detect_compress_method('test/test.tar'))
        lst = list_tar('test/test.tar.gz')
        self.assertEqual(len(lst), 2)
        self.assertEqual(lst[0].path, 'test.json')
        self.assertEqual(lst[1].path, 'test.json.gz')
        extract_tar_file('test/test.tar.gz', 'test/test2.json', 'test.json')
        self.assertEqual(True, exists('test/test2.json'))
        mkdir('data')
        extract_tar_file('test/test.tar.gz', 'data/', 'test.json')
        self.assertEqual(True, exists('data/test.json'))
        remove_files('data/test.json')
        file = open_tar_file('test/test.tar.gz', 'test.json')
        d2 = json.load(file)
        self.assertDictEqual(d, d2)
        file.close()
        remove_files('data')
        d2 = open_tar_json('test/test.tar.gz', 'test.json.gz')
        self.assertDictEqual(d, d2)


if __name__ == '__main__':
    unittest.main()

import unittest

from mysutils.file import save_json, gzip_compress, gzip_decompress, load_json, remove_files


class MyTestCase(unittest.TestCase):
    def test_compress_gzip(self):
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


if __name__ == '__main__':
    unittest.main()

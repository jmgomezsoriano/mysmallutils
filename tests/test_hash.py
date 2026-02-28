import unittest
from mysutils.hash import file_md5, file_sha1, file_sha224, file_sha256, file_sha384, file_sha512
from mysutils.file import write_file
from mysutils.tmp import removable_tmp


class MyTestCase(unittest.TestCase):
    def test_hash_codes(self):
        with removable_tmp() as tmp:
            write_file(tmp, 'Hello World!')
            self.assertEqual(file_md5(tmp), 'ed076287532e86365e841e92bfc50d8c')
            self.assertEqual(file_sha1(tmp), '2ef7bde608ce5404e97d5f042f95f89f1c232871')
            self.assertEqual(file_sha224(tmp), '4575bb4ec129df6380cedde6d71217fe0536f8ffc4e18bca530a7a1b')
            self.assertEqual(file_sha256(tmp), '7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069')
            self.assertEqual(
                file_sha384(tmp),
                'bfd76c0ebbd006fee583410547c1887b0292be76d582d96c242d2a792723e3fd6fd061f9d5cfd13b8f961358e6adba4a')
            self.assertEqual(
                file_sha512(tmp),
                '861844d6704e8573fec34d967e20bcfef3d424cf48be04e6dc08f2bd58c729743371015ead891cc3cf1c9d34b49264b510751b1ff9e537937bc46b5d6ff4ecc8')
            # Check with other buffer size
            self.assertEqual(file_md5(tmp, buffer_size=65535), 'ed076287532e86365e841e92bfc50d8c')
            self.assertEqual(file_sha1(tmp, buffer_size=65535), '2ef7bde608ce5404e97d5f042f95f89f1c232871')
            self.assertEqual(file_sha224(tmp, buffer_size=65535),
                             '4575bb4ec129df6380cedde6d71217fe0536f8ffc4e18bca530a7a1b')
            self.assertEqual(file_sha256(tmp, buffer_size=65535),
                             '7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069')
            # Check with binary format
            self.assertEqual(file_md5(tmp, False), b'\xed\x07b\x87S.\x866^\x84\x1e\x92\xbf\xc5\r\x8c')
            self.assertEqual(file_sha1(tmp, False), b'.\xf7\xbd\xe6\x08\xceT\x04\xe9}_\x04/\x95\xf8\x9f\x1c#(q')
            self.assertEqual(file_sha224(tmp, False),
                             b'Eu\xbbN\xc1)\xdfc\x80\xce\xdd\xe6\xd7\x12\x17\xfe\x056\xf8\xff\xc4\xe1\x8b\xcaS\nz\x1b')
            self.assertEqual(file_sha256(tmp, False),
                             b'\x7f\x83\xb1e\x7f\xf1\xfcS\xb9-\xc1\x81H\xa1\xd6]\xfc-K\x1f\xa3\xd6w(J\xdd\xd2\x00\x12m\x90i')
            self.assertEqual(
                file_sha384(tmp, False),
                b"\xbf\xd7l\x0e\xbb\xd0\x06\xfe\xe5\x83A\x05G\xc1\x88{\x02\x92\xbev\xd5\x82\xd9l$-*y'#\xe3\xfdo\xd0a\xf9\xd5\xcf\xd1;\x8f\x96\x13X\xe6\xad\xbaJ"
            )
            self.assertEqual(
                file_sha512(tmp, False),
                b'\x86\x18D\xd6pN\x85s\xfe\xc3M\x96~ \xbc\xfe\xf3\xd4$\xcfH\xbe\x04\xe6\xdc\x08\xf2\xbdX\xc7)t3q\x01^\xad\x89\x1c\xc3\xcf\x1c\x9d4\xb4\x92d\xb5\x10u\x1b\x1f\xf9\xe57\x93{\xc4k]o\xf4\xec\xc8'
            )
            # Check with binary format and different buffer size
            self.assertEqual(file_md5(tmp, False, 65535), b'\xed\x07b\x87S.\x866^\x84\x1e\x92\xbf\xc5\r\x8c')
            self.assertEqual(file_sha1(tmp, False, 65535), b'.\xf7\xbd\xe6\x08\xceT\x04\xe9}_\x04/\x95\xf8\x9f\x1c#(q')
            self.assertEqual(file_sha224(tmp, False, 65535),
                             b'Eu\xbbN\xc1)\xdfc\x80\xce\xdd\xe6\xd7\x12\x17\xfe\x056\xf8\xff\xc4\xe1\x8b\xcaS\nz\x1b')
            self.assertEqual(file_sha256(tmp, False, 65535),
                             b'\x7f\x83\xb1e\x7f\xf1\xfcS\xb9-\xc1\x81H\xa1\xd6]\xfc-K\x1f\xa3\xd6w(J\xdd\xd2\x00\x12m\x90i')
            self.assertEqual(
                file_sha384(tmp, False, 65535),
                b"\xbf\xd7l\x0e\xbb\xd0\x06\xfe\xe5\x83A\x05G\xc1\x88{\x02\x92\xbev\xd5\x82\xd9l$-*y'#\xe3\xfdo\xd0a\xf9\xd5\xcf\xd1;\x8f\x96\x13X\xe6\xad\xbaJ"
            )
            self.assertEqual(
                file_sha512(tmp, False, 65535),
                b'\x86\x18D\xd6pN\x85s\xfe\xc3M\x96~ \xbc\xfe\xf3\xd4$\xcfH\xbe\x04\xe6\xdc\x08\xf2\xbdX\xc7)t3q\x01^\xad\x89\x1c\xc3\xcf\x1c\x9d4\xb4\x92d\xb5\x10u\x1b\x1f\xf9\xe57\x93{\xc4k]o\xf4\xec\xc8'
            )
            # Check if the codes change when I change the content of the file
            write_file(tmp, 'Hello World 2!')
            self.assertNotEqual(file_md5(tmp), 'ed076287532e86365e841e92bfc50d8c')
            self.assertNotEqual(file_sha1(tmp), '2ef7bde608ce5404e97d5f042f95f89f1c232871')
            self.assertNotEqual(file_sha224(tmp), '4575bb4ec129df6380cedde6d71217fe0536f8ffc4e18bca530a7a1b')
            self.assertNotEqual(file_sha256(tmp), '7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069')
            self.assertNotEqual(
                file_sha384(tmp),
                'bfd76c0ebbd006fee583410547c1887b0292be76d582d96c242d2a792723e3fd6fd061f9d5cfd13b8f961358e6adba4a')
            self.assertNotEqual(
                file_sha512(tmp),
                '861844d6704e8573fec34d967e20bcfef3d424cf48be04e6dc08f2bd58c729743371015ead891cc3cf1c9d34b49264b510751b1ff9e537937bc46b5d6ff4ecc8')


if __name__ == '__main__':
    unittest.main()

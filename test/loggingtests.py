import unittest
from logging import getLogger

from mysutils.file import first_line, remove_files
from mysutils.logging import get_log_level_names, get_log_levels, get_log_level, config_log

config_log('ERROR', 'file.log')
logger = getLogger(__name__)


def log_messages() -> None:
    logger.info('Test info message')
    logger.warning('Test warning message')
    logger.error('Test error message')


class MyTestCase(unittest.TestCase):
    def test_config_logging(self):
        with self.assertLogs(logger, 'ERROR') as cm:
            log_messages()
        self.assertEqual(cm.output, ['ERROR:__main__:Test error message'])
        log_messages()
        msg = first_line('file.log')
        self.assertEqual(msg[-18:], 'Test error message')
        remove_files('file.log')

    def test_log_level_names(self) -> None:
        self.assertListEqual(get_log_level_names(),
                             ['critical', 'fatal', 'error', 'warn', 'warning', 'info', 'debug', 'notset'])

    def test_log_levels(self) -> None:
        self.assertListEqual(get_log_levels(), [('CRITICAL', 50), ('FATAL', 50), ('ERROR', 40), ('WARN', 30),
                                                ('WARNING', 30), ('INFO', 20), ('DEBUG', 10), ('NOTSET', 0)])

    def test_log_level(self) -> None:
        self.assertEqual(get_log_level('DEBUG'), 10)


if __name__ == '__main__':
    unittest.main()

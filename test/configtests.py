import unittest

from mysutils.config import parse_config

PARAM_DEFINITION = [('server_host', False, 'http://0.0.0.0'), ('server_port', False, 8080),
                    ('database_name', True, None)]


class MyTestCase(unittest.TestCase):
    def test_correct_config(self) -> None:
        # Check double check
        config = {
            'database_name': 'Test'
        }
        values = parse_config(config, PARAM_DEFINITION, True)
        self.assertTupleEqual(values, ('http://0.0.0.0', 8080, 'Test'))
        # Check without double check
        config = {
            'database_name': 'Test',
            'new_parameter': 1
        }
        values = parse_config(config, PARAM_DEFINITION, False)
        self.assertTupleEqual(values, ('http://0.0.0.0', 8080, 'Test'))

    def test_wrong_double_check_config(self) -> None:
        # Check correct double check
        config = {
            'database_name': 'Test'
        }
        values = parse_config(config, PARAM_DEFINITION, True)
        self.assertTupleEqual(values, ('http://0.0.0.0', 8080, 'Test'))
        # Check failure double check
        config = {
            'database_name': 'Test',
            'new_parameter': 1
        }
        with self.assertRaises(ValueError):
            parse_config(config, PARAM_DEFINITION, True)

    def test_required_config(self) -> None:
        config = {
            'new_parameter': 1
        }
        # Check double check
        with self.assertRaises(ValueError) as e:
            parse_config(config, PARAM_DEFINITION, True)
        self.assertEqual(str(e.exception),
                         'The parameter "new_parameter" in the configuration file is not a valid parameter.')
        # Check if the parameter config
        with self.assertRaises(ValueError) as e:
            parse_config(config, PARAM_DEFINITION, False)
        self.assertEqual(str(e.exception),
                         'The parameter "database_name" is not defined in the configuration file and it is mandatory.')


if __name__ == '__main__':
    unittest.main()

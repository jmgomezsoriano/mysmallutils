import unittest
from unittest import TestCase

from mysutils.time import format_shorthand, countdown_timer
from unittest.mock import patch, MagicMock


class TestTime(TestCase):
    def test_full_duration(self):
        self.assertEqual(format_shorthand(1, 2, 30, 45), "1d 2h 30m 45s")

    def test_missing_middle_units(self):
        self.assertEqual(format_shorthand(5, 0, 0, 10), "5d 10s")

    def test_single_unit(self):
        self.assertEqual(format_shorthand(0, 0, 15, 0), "15m")

    def test_all_zeros(self):
        self.assertEqual(format_shorthand(0, 0, 0, 0), "")

    def test_large_values(self):
        self.assertEqual(format_shorthand(365, 24, 60, 60), "365d 24h 60m 60s")


class TestCountdownTimer(TestCase):
    @patch('time.sleep', return_value=None)
    @patch('mysutils.time.tqdm')
    def test_timer_calls_update(self, mock_tqdm, mock_sleep):
        # Configuramos el mock
        mock_pbar = MagicMock()
        mock_tqdm.return_value.__enter__.return_value = mock_pbar

        countdown_timer(2.5)

        self.assertEqual(mock_pbar.update.call_count, 3)

        last_call_args = mock_pbar.update.call_args_list[-1]
        self.assertEqual(last_call_args[0][0], 0.5)

    def test_timer_zero_seconds(self):
        with patch('tqdm.tqdm') as mock_tqdm:
            countdown_timer(0)
            mock_tqdm.return_value.__enter__.return_value.update.assert_not_called()

if __name__ == '__main__':
    unittest.main()

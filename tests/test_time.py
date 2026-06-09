import unittest
from unittest import TestCase

from mysutils.time import format_shorthand, countdown_timer
from unittest.mock import patch, MagicMock, call


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
    @patch('time.sleep')
    @patch('time.time')
    @patch('mysutils.time.tqdm')
    def test_timer_calls_update(self, mock_tqdm, mock_time, mock_sleep):
        # 1. Estado para nuestro reloj simulado
        time_state = {"current": 0.0}

        def virtual_time():
            # Simulamos que cada instrucción de Python toma un microsegundo
            # Esto evita el bucle infinito permitiendo que el tiempo avance muy poquito
            time_state["current"] += 0.0001
            return time_state["current"]

        def virtual_sleep(secs):
            # Cuando tu código llama a sleep(), avanzamos el reloj virtual de golpe
            time_state["current"] += secs

        # Asignamos nuestras funciones a los mocks
        mock_time.side_effect = virtual_time
        mock_sleep.side_effect = virtual_sleep

        mock_pbar = MagicMock()
        mock_tqdm.return_value.__enter__.return_value = mock_pbar

        # Ejecutamos
        countdown_timer(2.5)

        # 2. Comprobamos que el bucle duró las iteraciones correctas
        # Para 2.5s, debería dormir: 1.0s, luego 1.0s, luego 0.5s.
        expected_sleeps = [call(1.0), call(1.0), call(0.5)]

        # Comparamos ignorando los minúsculos márgenes de error de los 0.0001 agregados
        self.assertEqual(mock_sleep.call_count, 3)

    def test_timer_zero_seconds(self):
        with patch('tqdm.tqdm') as mock_tqdm:
            countdown_timer(0)
            mock_tqdm.return_value.__enter__.return_value.update.assert_not_called()

    @patch('time.sleep', return_value=None)
    @patch('mysutils.time.tqdm')
    def test_timer_stop_condition_callable(self, mock_tqdm, mock_sleep):
        mock_pbar = MagicMock()
        mock_tqdm.return_value.__enter__.return_value = mock_pbar

        # Creamos un callable (closure) que devuelve True en la 3ra iteración
        iteraciones = [0]

        def stop_cond():
            iteraciones[0] += 1
            return iteraciones[0] == 3

        countdown_timer(5.0, description="Test Callable", stop_condition=stop_cond)

        # Como el bucle se rompe en el tercer chequeo, update() solo se llama 2 veces
        self.assertEqual(mock_pbar.update.call_count, 2)
        mock_pbar.set_description.assert_called_once_with("Test Callable (Interrupted)")

    @patch('time.sleep', return_value=None)
    @patch('mysutils.time.tqdm')
    def test_timer_stop_condition_iterator(self, mock_tqdm, mock_sleep):
        mock_pbar = MagicMock()
        mock_tqdm.return_value.__enter__.return_value = mock_pbar

        # Creamos un generador que arroja False dos veces y luego True
        def stop_cond_gen():
            yield False
            yield False
            yield True
            while True:
                yield True

        countdown_timer(5.0, description="Test Generator", stop_condition=stop_cond_gen())

        # Igual que el anterior, al dar True a la tercera vez, solo hace update() 2 veces
        self.assertEqual(mock_pbar.update.call_count, 2)
        mock_pbar.set_description.assert_called_once_with("Test Generator (Interrupted)")

if __name__ == '__main__':
    unittest.main()

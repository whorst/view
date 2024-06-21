import unittest
from unittest.mock import patch, Mock
import datetime, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'asciirequester')))
from scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    def test_get_iso_week(self):
        datetime_mock = Mock(wraps=datetime.date)
        datetime_mock.today.return_value = datetime.datetime(1999, 1, 1)
        with patch('datetime.date', new=datetime_mock):
            scheduler = Scheduler()
            iso_week = scheduler.get_iso_week()
            self.assertEqual(iso_week, 53)

    def test_get_delay_in_seconds_odd_week(self):
        datetime_mock = Mock(wraps=datetime.date)
        datetime_mock.today.return_value = datetime.datetime(1999, 1, 1)
        with patch('datetime.date', new=datetime_mock):
            scheduler = Scheduler()
            delay = scheduler.get_delay_in_seconds()
            self.assertEqual(delay, 5)

    def test_get_delay_in_seconds_even_week(self):
        datetime_mock = Mock(wraps=datetime.date)
        datetime_mock.today.return_value = datetime.datetime(1999, 2, 11)
        with patch('datetime.date', new=datetime_mock):
            scheduler = Scheduler()
            delay = scheduler.get_delay_in_seconds()
            self.assertEqual(delay, 10)

    # Mocking sleep to avoid actual delay
    @patch('time.sleep', return_value=None)
    @patch('sys.stdout.flush', return_value=None)  # Mocking stdout flush
    def test_schedule_task_exception(self, mock_flush, mock_sleep):
        scheduler = Scheduler()

        mocked_object = Mock()

        mocked_object.schedule_task = Mock()
        mocked_object.schedule_task.side_effect = Exception(
            "An error occurred")

        scheduler.schedule_task(mocked_object)

        mock_flush.assert_not_called()
        mock_sleep.assert_not_called()

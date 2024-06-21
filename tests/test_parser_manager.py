from unittest import TestCase
from unittest.mock import Mock, patch
import sys
import os
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'asciirequester')))

from server.server import Server
from parsers.parser_manager import NumberParser, LetterParser, ParserManager

class TestParserManager(TestCase):
    def setUp(self):
        self.mock_container = Mock()
        self.parser_manager = ParserManager(
            Server("abcd", "123", self.mock_container),
            Server("abcd", "123", self.mock_container)
        )

    @patch.object(NumberParser, 'get_numbers_total')
    @patch.object(LetterParser, 'process_numbers')
    def test_schedule_task_success(
            self,
            mock_process_numbers,
            mock_get_numbers_total):
        self.mock_container.get_server_response.side_effect = ['1', 'abcd']

        mock_get_numbers_total.return_value = 1
        self.parser_manager.schedule_task()

        mock_get_numbers_total.assert_called_once()
        mock_process_numbers.assert_called_once()

    def test_schedule_task_exception_raised_when_number_retrieval_fails(self):
        self.mock_container.get_server_response.side_effect = [None]

        with self.assertRaises(Exception) as context:
            self.parser_manager.schedule_task()
        self.assertEqual(str(context.exception),
                         "Could not get the response from the number server")

    @patch.object(NumberParser, 'get_numbers_total')
    @patch.object(LetterParser, 'process_numbers')
    def test_schedule_task_exception_raised_when_letter_retrieval_fails(
            self, mock_process_numbers, mock_get_numbers_total):
        self.mock_container.get_server_response.side_effect = ['1', None]
        mock_get_numbers_total.return_value = 1
        with self.assertRaises(Exception) as context:
            self.parser_manager.schedule_task()
        self.assertEqual(str(context.exception),
                         "Could not get the response from the letter server")

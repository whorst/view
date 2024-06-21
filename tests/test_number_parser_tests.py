from unittest import TestCase
import sys
import os
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'asciirequester')))
from parsers.number_parser import NumberParser


class TestNumberParser(TestCase):

    def setUp_number_parser(self, numbers):
        return NumberParser(numbers)

    def test_parse_numbers_valid(self):
        parser = self.setUp_number_parser("1052")
        self.assertEqual(parser.get_numbers_total(), 8)

    def test_parse_numbers_with_invalid(self):
        parser = self.setUp_number_parser("105a2")
        self.assertEqual(parser.get_numbers_total(), 0)

    def test_parse_numbers_empty_list(self):
        parser = self.setUp_number_parser(None)
        self.assertEqual(parser.get_numbers_total(), 0)

    def test_parse_numbers_all_invalid(self):
        parser = self.setUp_number_parser("abcdefxyz")
        self.assertEqual(parser.get_numbers_total(), 0)

    def test_parse_numbers_single_number(self):
        parser = self.setUp_number_parser("10")
        self.assertEqual(parser.get_numbers_total(), 1)

    def test_parse_numbers_multiple_zeros(self):
        parser = self.setUp_number_parser("000000")
        self.assertEqual(parser.get_numbers_total(), 0)
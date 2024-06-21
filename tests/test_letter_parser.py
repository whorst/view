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
from parsers.letter_parser import LetterParser


class TestLetterParser(TestCase):

    def setUp_letter_parser(self, input_string, modify_counter=None):
        letter_parser = LetterParser()
        letter_parser.process_numbers(input_string)
        if modify_counter:
            for idx, val in modify_counter.items():
                letter_parser._letter_counter_list[idx] = val
        return letter_parser

    def test_format_occurrences(self):
        letter_parser = self.setUp_letter_parser("aabccc")
        expected_output = "2 1 3\na b c d e f g h i j k l m n o p q r s t u v w x y z"
        self.assertEqual(letter_parser.format_occurrences(), expected_output)

    def test_format_occurrences_all_zeros(self):
        letter_parser = self.setUp_letter_parser("")
        expected_output = "\na b c d e f g h i j k l m n o p q r s t u v w x y z"
        self.assertEqual(letter_parser.format_occurrences(), expected_output)

    def test_format_occurrences_with_dd_provided_input(self):
        letter_parser = self.setUp_letter_parser("demoengineeringteam")
        expected_output = "1     1 5   2   2       2 3 1     1   1\na b c d e f g h i j k l m n o p q r s t u v w x y z"
        self.assertEqual(letter_parser.format_occurrences(), expected_output)

    def test_format_occurrences_with_quad_digits_count(self):
        letter_parser = self.setUp_letter_parser("demoengineeringteam", modify_counter={0: 1000})
        expected_output = "1000     1 5   2   2       2 3 1     1   1\na    b c d e f g h i j k l m n o p q r s t u v w x y z"
        self.assertEqual(letter_parser.format_occurrences(), expected_output)

    def test_format_occurrences_with_triple_and_quad_digit_count(self):
        letter_parser = self.setUp_letter_parser("demoengineeringteam", modify_counter={1: 1000, 4: 333})
        expected_output = "1 1000   1 333   2   2       2 3 1     1   1\na b    c d e   f g h i j k l m n o p q r s t u v w x y z"
        self.assertEqual(letter_parser.format_occurrences(), expected_output)

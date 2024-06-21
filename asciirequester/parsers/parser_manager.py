import sys

from .number_parser import NumberParser
from .letter_parser import LetterParser


class ParserManager:
    def __init__(self, number_server, letter_server):
        """
        Initialize ParserManager. This class is meant to handle the number and
        letter parsing operations and the control flow for actually making it so the parsing can
        be executed, as well as the logging of the letter counts. One can kind of think
        of this class like the Mediator design pattern

        Parameters:
        number_server (Server): Instance of the number server.
        letter_server (Server): Instance of the letter server.

        """
        self.number_server = number_server
        self.letter_server = letter_server

    def schedule_task(self):
        """
        Schedule a task to fetch responses from servers, parse them, and log the results. This method is
        called by the scheduler class to run indefinitely

        Raises:
        Exception: If failed to get response from either number or letter server.
        """
        number_response = self.number_server.get_server_response()
        if not number_response:
            raise Exception(
                "Could not get the response from the number server")

        if number_response:
            number_parser = NumberParser(number_response)
            total = number_parser.get_numbers_total()

            letter_parser = LetterParser()
            self.build_letter_response(letter_parser, total)
            output = letter_parser.format_occurrences()
            self.log_letter_map(output, total)

        sys.stdout.flush()

    def build_letter_response(self, letter_parser, total):
        """
        Build response from letter server. The main responsibility of
        this method is to get the response from the letter server and
        have that response be parsed by the letter parser class.


        Parameters:
        letter_parser: An instance of LetterParser class.
        total (int): Total number of requests to letter server.

        Raises:
        Exception: If failed to get response from the letter server.
        """
        i = 0
        while i < total:
            letter_response = self.letter_server.get_server_response()

            if not letter_response:
                raise Exception(
                    "Could not get the response from the letter server")
            letter_parser.process_numbers(letter_response)
            i += 1

    def log_message(self, message, *args):
        print(message.format(*args))

    def log_letter_map(self, output, total):
        self.log_message("Strings: {}", total)
        self.log_message("Character Counts:")
        self.log_message(output)
        self.log_message("")

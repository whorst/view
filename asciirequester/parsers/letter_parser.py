class LetterParser:
    def __init__(self):
        """
        Initialize LetterParser.

        Initializes the LetterParser object with a list to count occurrences of each letter. The LetterParser object will
        take in responses from the letters server and parse and format them
        """
        self._letter_counter_list = [0] * 26

    def process_numbers(self, letter_response):
        """
        Process the response from the letter server.

        Counts the occurrences of each letter in the response and save it to the letter_counter_list.

        Parameters:
        letter_response (str): The response received from the letter server.
        """
        for letter in letter_response:
            index = ord(letter) - ord('a')
            self._letter_counter_list[index] += 1

    def format_occurrences(self):
        """
        Format the occurrences of each letter.

        Returns a string with occurrences of each letter along with the corresponding alphabet.

        Returns:
        str: A string containing the formatted occurrences of each letter.
        """
        numbers_line = ''
        alphabet_line = ''

        for index, count in enumerate(self._letter_counter_list):
            num_str = str(count) if count != 0 else ' '
            numbers_line += num_str + ' '
            char = chr(ord('a') + index)
            total_padding = len(num_str)
            alphabet_line += char + (' ' * total_padding)

        numbers_line = numbers_line.rstrip()
        return numbers_line + '\n' + alphabet_line.strip()

class NumberParser:
    def __init__(self, numbers):
        """
        Initialize NumberParser.

        Initializes the NumberParser object with a list of numbers and calculates the total if numbers are provided.

        Parameters:
        numbers (list): A list of numbers (as strings) to parse and calculate the total.
        """
        self.numbers = numbers
        self._numbers_total = 0
        if self.numbers is not None:
            self.parse_numbers()

    def parse_numbers(self):
        """
        Parse the numbers and calculate the total.

        Converts each number from string to integer and calculates the total if all numbers are valid digits.
        If any non-digit is encountered, sets the total to 0.

        """
        total = 0
        for num in self.numbers:
            if num.isdigit():
                num = int(num)
                total += num
            else:
                self._numbers_total = 0
                return
        self._numbers_total = total

    def get_numbers_total(self):
        """
        Get the total of parsed numbers.

        Returns:
        int: The total sum of parsed numbers.
        """
        return self._numbers_total

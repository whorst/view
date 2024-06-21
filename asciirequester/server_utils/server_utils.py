import subprocess
import os
from .server_logging import log_message

NUMBERS_PORT = 'NUMBERS_PORT'
NUMBERS_ADDRESS = 'NUMBERS_ADDRESS'
LETTERS_PORT = 'LETTERS_PORT'
LETTERS_ADDRESS = 'LETTERS_ADDRESS'


class ServerUtils:
    """
    This class contains utilities for communication between containers
    """

    @staticmethod
    def is_valid_port_number(port_number):
        """
        Validate if the given port number is an integer within the range 0-65535.

        Parameters:
        port_number: The port number to be validated. It can be of any type that can be cast to an integer.

        Returns:
        bool: True if the port number is valid (i.e., an integer within the range 0-65535).
        None: If the port number is invalid.

        Exceptions:
        The method logs a message if the port number is invalid (either not an integer or out of the valid range).
        """
        try:
            port = int(port_number)
            if 0 <= port <= 65535:
                return True
        except Exception:
            log_message("Invalid port number: {}", port_number)
        log_message("Invalid port number: {}", port_number)
        return None

    @staticmethod
    def is_valid_server_address(address) -> bool:
        """
        Validate if the given server address is valid.

        A valid server address must:
        - Be non-empty.
        - Start with an alphanumeric character.
        - Contain only alphanumeric characters, underscores ('_'), hyphens ('-'), or periods ('.').

        Parameters:
        address: The Docker server_utils address or 'localhost' to be validated (str).

        Returns:
        bool: True if the server address is valid.
        False: If the server address is invalid.
        """
        if not address:
            log_message("Failed: Invalid server address, none provided")
            return False
        if not address[0].isalnum():
            log_message(
                "Failed: Invalid server address, first character must be alphanumeric: {}",
                address)
            return False
        for char in address:
            if not (char.isalnum() or char in ['_', '-', '.']):
                log_message(
                    "Failed: Invalid server address, non-allowed character found: {}, {}",
                    char,
                    address)
                return False
        return True

    @staticmethod
    def build_server_address(address, port):
        """
        Build the url for a server given its address and port.

        This method constructs a URL in the format "http://{address}:{port}" if the server address
        and port number are valid.

        Parameters:
        address: The server address to be validated (str).
        port: The port number to be validated (int or str).

        Returns:
        str: The constructed server address in the format "http://{address}:{port}" if both
             the server address and port number are valid.
        None: If either the server address or the port number is invalid.
        """
        if address is not None and port is not None:
            server_address = f"http://{address}:{port}"
            return server_address
        return None

    @staticmethod
    def get_server_response(address, port):
        """
        Get the response from a server given its address and port.

        This method constructs the server address using the `build_server_address` method and
        then uses the `run_curl` method to fetch the response from the constructed address.

        Parameters:
        address: The address of the server to be validated (str).
        port: The port number to be validated (int or str).

        Returns:
        The result of the `run_curl` method if the server address is valid.
        None: If the server address is invalid.
        """
        server_address = ServerUtils.build_server_address(address, port)
        result = None
        if server_address:
            result = ServerUtils.run_curl(server_address)
        return result

    @staticmethod
    def run_curl(address):
        """
        Execute a curl command to fetch the response from the specified address.

        This method constructs and runs a curl command to the provided address and returns the command's output if successful.
        If the curl command fails or an exception occurs, it logs an appropriate message and returns None.

        Parameters:
        address: The address to fetch the response from (str).

        Returns:
        str: The stdout of the curl command if the command executes successfully.
        None: If the curl command fails (non-zero return code) or an exception occurs.
        """
        try:
            curl_command = ["curl", address]
            result = subprocess.run(
                curl_command, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                log_message(
                    "Failed: Curl failure with return code: {}, result: {}",
                    result.returncode,
                    result)
                return None
        except Exception as e:
            log_message(
                "Failed: Received exception when running curl with address {}: {}",
                address,
                e)
            return None

    @staticmethod
    def get_server_address_and_port(address_variable, port_variable):
        """
        Retrieve the server address and port from environment variables.

        This method fetches the server address and port number from the specified environment variables. If both variables
        are found, it returns them. If either variable is not found, it logs an appropriate message and returns None for both.

        Parameters:
        address_variable: The address of the environment variable that holds the server address (str).
        port_variable: The address of the environment variable that holds the server port (str).

        Returns:
        tuple: A tuple containing the server address and server port if both are found.
        (None, None): If either the server address or server port is not found.
        """
        server_address = os.environ.get(address_variable)
        server_port = os.environ.get(port_variable)

        server_address_valid = ServerUtils.is_valid_server_address(
            server_address)
        port_number_valid = ServerUtils.is_valid_port_number(server_port)

        if server_address and server_port and server_address_valid and port_number_valid:
            return server_address, server_port
        log_message(
            "Failed to get environment variable: {}, returned value: {}",
            address_variable,
            server_address)
        log_message(
            "Failed to get environment variable: {}, returned value: {}",
            port_variable,
            server_port)
        return None, None

    @staticmethod
    def get_letter_server_info():
        return ServerUtils.get_server_address_and_port(
            LETTERS_ADDRESS, LETTERS_PORT)

    @staticmethod
    def get_number_server_info():
        return ServerUtils.get_server_address_and_port(
            NUMBERS_ADDRESS, NUMBERS_PORT)

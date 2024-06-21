class Server:
    """
    A class to represent a server with a specific address and port, which interacts with a server_utils.

    Attributes:
    ----------
    address : str
        The address of the server.
    port : int
        The port number of the server.
    server_utils : object
        The server_utils object that the server interacts with to get responses.

    Methods:
    -------
    get_server_response():
        Retrieves the response from the server_utils for the given server address and port.
    """

    def __init__(self, address, port, container):
        """
        Constructs all the necessary attributes for the Server object.

        Parameters:
        ----------
        address : str
            The address of the server.
        port : int
            The port number of the server.
        server_utils : object
            The server_utils object that the server interacts with to get responses.
        """
        self._address = address
        self._port = port
        self._container = container

    def get_server_response(self):
        """
        Retrieves the response from the server for the given server address and port.

        Returns:
        -------
        response : object
            The response from the server_utils curl.
        """
        response = self._container.get_server_response(
            self._address, self._port)
        return response

from server.server import Server
from server_utils.server_utils import ServerUtils
from parsers.parser_manager import ParserManager
from scheduler import Scheduler

container = ServerUtils

letter_address, letter_port = container.get_letter_server_info()
number_address, number_port = container.get_number_server_info()


if letter_address and number_address:
    scheduler = Scheduler()
    letter_server = Server(letter_address, letter_port, container)
    number_server = Server(number_address, number_port, container)
    parser_manager = ParserManager(number_server, letter_server)
    scheduler.schedule_task(parser_manager)

from unittest import TestCase
from unittest.mock import patch, Mock
import sys
import os
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'asciirequester')))
from server_utils.server_utils import ServerUtils


class TestGetContainerResponse(TestCase):
    def setUp(self):
        self.obj = ServerUtils

    @patch.object(ServerUtils, 'build_server_address')
    @patch.object(ServerUtils, 'run_curl')
    def test_get_container_response_success(
            self, mock_run_curl, mock_build_container_address):
        mock_build_container_address.return_value = "http://validname:8080"
        mock_run_curl.return_value = "Success"

        result = self.obj.get_server_response("validname", 8080)
        self.assertEqual(result, "Success")

    @patch.object(ServerUtils, 'build_server_address')
    def test_get_container_response_invalid_address(
            self, mock_build_container_address):
        mock_build_container_address.return_value = None

        result = self.obj.get_server_response("invalidname", 8080)
        self.assertIsNone(result)

    @patch.object(ServerUtils, 'build_server_address')
    @patch.object(ServerUtils, 'run_curl')
    def test_get_container_response_curl_failure(
            self, mock_run_curl, mock_build_container_address):
        mock_build_container_address.return_value = "http://validname:8080"
        mock_run_curl.return_value = None

        result = self.obj.get_server_response("validname", 8080)
        self.assertIsNone(result)


class TestRunCurl(TestCase):
    def setUp(self):
        self.obj = ServerUtils

    @patch('subprocess.run')
    def test_run_curl_success(self, mock_run):
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Success"
        mock_run.return_value = mock_result

        result = self.obj.run_curl("http://example.com")
        self.assertEqual(result, "Success")

    @patch('subprocess.run')
    def test_run_curl_failure(self, mock_run):
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = "Error output"
        mock_result.stderr = "Error message"
        mock_run.return_value = mock_result

        result = self.obj.run_curl("http://example.com")
        self.assertIsNone(result)

    @patch('subprocess.run')
    def test_run_curl_exception(self, mock_run):
        mock_run.side_effect = Exception("Exception message")

        result = self.obj.run_curl("http://example.com")
        self.assertIsNone(result)


class TestGetServer(TestCase):
    def setUp(self):
        self.obj = ServerUtils

    @patch('os.environ.get')
    def test_valid_environment_variables(self, mock_get):
        mock_get.side_effect = lambda var: {
            'NAME_VAR': 'server_name',
            'PORT_VAR': '8080'
        }.get(var, None)

        server_name, server_port = self.obj.get_server_address_and_port(
            'NAME_VAR', 'PORT_VAR')
        self.assertEqual(server_name, 'server_name')
        self.assertEqual(server_port, '8080')

    @patch('os.environ.get')
    def test_missing_name_variable(self, mock_get):
        mock_get.side_effect = lambda var: {
            'NAME_VAR': None,
            'PORT_VAR': '8080'
        }.get(var, None)

        server_name, server_port = self.obj.get_server_address_and_port(
            'NAME_VAR', 'PORT_VAR')
        self.assertIsNone(server_name)
        self.assertIsNone(server_port)

    @patch('os.environ.get')
    def test_missing_port_variable(self, mock_get):
        mock_get.side_effect = lambda var: {
            'NAME_VAR': 'server_name',
            'PORT_VAR': None
        }.get(var, None)

        server_name, server_port = self.obj.get_server_address_and_port(
            'NAME_VAR', 'PORT_VAR')
        self.assertIsNone(server_name)
        self.assertIsNone(server_port)

    @patch('os.environ.get')
    def test_missing_both_variables(self, mock_get):
        mock_get.side_effect = lambda var: None

        server_name, server_port = self.obj.get_server_address_and_port(
            'NAME_VAR', 'PORT_VAR')
        self.assertIsNone(server_name)
        self.assertIsNone(server_port)


class TestBuildContainerAddress(TestCase):
    def setUp(self):
        self.obj = ServerUtils

    def test_valid_address(self):
        self.assertEqual(
            self.obj.build_server_address(
                "validname",
                8080),
            "http://validname:8080")
        self.assertEqual(
            self.obj.build_server_address(
                "valid-name",
                8080),
            "http://valid-name:8080")
        self.assertEqual(
            self.obj.build_server_address(
                "valid.name",
                8080),
            "http://valid.name:8080")


class TestIsValidDockerContainerName(TestCase):
    def setUp(self):
        self.obj = ServerUtils

    def test_valid_server_address(self):
        self.assertTrue(self.obj.is_valid_server_address("valid_name"))
        self.assertTrue(self.obj.is_valid_server_address("valid-name"))
        self.assertTrue(self.obj.is_valid_server_address("valid.name"))
        self.assertTrue(self.obj.is_valid_server_address("validname"))

    def test_invalid_server_address_none(self):
        self.assertFalse(self.obj.is_valid_server_address(None))

    def test_invalid_server_address_empty_string(self):
        self.assertFalse(self.obj.is_valid_server_address(""))

    def test_invalid_server_address_non_alphanumeric_start(self):
        self.assertFalse(self.obj.is_valid_server_address("_invalid"))

    def test_invalid_server_address_non_allowed_character(self):
        self.assertFalse(self.obj.is_valid_server_address("invalid@name"))


class TestContainer_is_valid_port_number(TestCase):

    def setUp(self):
        self.obj = ServerUtils

    def test_valid_port_number_0(self):
        self.assertTrue(self.obj.is_valid_port_number(0))

    def test_valid_port_number_80(self):
        self.assertTrue(self.obj.is_valid_port_number(80))

    def test_valid_port_number_65535(self):
        self.assertTrue(self.obj.is_valid_port_number(65535))

    def test_invalid_port_number_minus_1(self):
        self.assertFalse(self.obj.is_valid_port_number(-1))

    def test_invalid_port_number_65536(self):
        self.assertFalse(self.obj.is_valid_port_number(65536))

    def test_invalid_port_number_not_a_number(self):
        self.assertFalse(self.obj.is_valid_port_number("not_a_number"))

    def test_edge_case_none(self):
        self.assertFalse(self.obj.is_valid_port_number(None))

    def test_edge_case_empty_string(self):
        self.assertFalse(self.obj.is_valid_port_number(""))

    def test_edge_case_space(self):
        self.assertFalse(self.obj.is_valid_port_number(" "))

    def test_edge_case_string_65536(self):
        self.assertFalse(self.obj.is_valid_port_number("65536"))

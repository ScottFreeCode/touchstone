import json
import urllib
import urllib.error
import urllib.parse
import urllib.request

from touchstone.lib import exceptions
from touchstone.lib.configs.touchstone_config import TouchstoneConfig
from touchstone.lib.mocks.mock_case import Setup


class HttpSetup(Setup):
    def __init__(self, exposed_port: int):
        super().__init__(exposed_port)
        self.mock_ids: list = []

    def cleanup(self):
        # Remove all mocked endpoints
        for mock_id in self.mock_ids:
            request = urllib.request.Request(
                f'http://{TouchstoneConfig.instance().config["host"]}:{self.exposed_port}/__admin/mappings/'
                f'{mock_id}',
                method='DELETE')
            urllib.request.urlopen(request)
        self.mock_ids = []

        # Reset requests journal
        request = urllib.request.Request(
            f'http://{TouchstoneConfig.instance().config["host"]}:{self.exposed_port}/__admin/requests',
            method='DELETE')
        urllib.request.urlopen(request)

    def load_defaults(self, defaults: dict):
        for default in defaults:
            self.__submit_mock(default)

    def get(self, endpoint: str, response: str, response_status: int = 200,
            response_headers: dict = {'Content-Type': 'application/json'}):
        """Returns the given response when a GET request is made to the given endpoint."""
        self.__check_mock_response_type(response)
        mock = {
            'request': {
                'method': 'GET',
                'url': endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_mock(mock)

    def post(self, endpoint: str, response: str, response_status: int = 200,
             response_headers: dict = {'Content-Type': 'application/json'}):
        """Returns the given response when a POST request is made to the given endpoint."""
        self.__check_mock_response_type(response)
        mock = {
            'request': {
                'method': 'POST',
                'url': endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_mock(mock)

    def put(self, endpoint: str, response: str, response_status: int = 200,
            response_headers: dict = {'Content-Type': 'application/json'}):
        """Returns the given response when a PUT request is made to the given endpoint."""
        self.__check_mock_response_type(response)
        mock = {
            'request': {
                'method': 'PUT',
                'url': endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_mock(mock)

    def delete(self, endpoint: str, response: str, response_status: int = 200,
               response_headers: dict = {'Content-Type': 'application/json'}):
        """Returns the given response when a DELETE request is made to the given endpoint."""
        self.__check_mock_response_type(response)
        mock = {
            'request': {
                'method': 'DELETE',
                'url': endpoint
            },
            'response': {
                'status': response_status,
                'headers': response_headers,
                'body': response
            }
        }
        self.__submit_mock(mock)

    def __check_mock_response_type(self, response):
        if type(response) is not str:
            raise exceptions.MockException('Response must be of type str.')

    def __submit_mock(self, mock: dict):
        data = json.dumps(mock).encode('utf8')
        request = urllib.request.Request(
            f'http://{TouchstoneConfig.instance().config["host"]}:{self.exposed_port}/__admin/mappings',
            data=data,
            headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        self.mock_ids.append(json.loads(response)['id'])

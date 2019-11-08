import http
import http.client
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict

import exceptions
from docker_manager import DockerManager
from mocks.mock import Mock
from touchstone_config import TouchstoneConfig


class Http(Mock):
    def __init__(self, mock_config):
        super().__init__(mock_config)
        self.mock_ids = []

    @staticmethod
    def name():
        return 'http'

    @staticmethod
    def pretty_name():
        return 'HTTP'

    def default_exposed_port(self):
        return 24080

    def is_healthy(self) -> bool:
        try:
            response = urllib.request.urlopen(
                f'http://{TouchstoneConfig.instance().config["host"]}:{self.exposed_port()}/__admin/mappings').read()
            return False if response is None else True
        except (urllib.error.URLError, http.client.RemoteDisconnected):
            return False

    def start(self):
        DockerManager.instance().run_image('rodolpheche/wiremock', self.exposed_port(), 8080)

    def load_defaults(self, defaults: Dict):
        for default in defaults:
            self.__submit_mock(default)

    def cleanup(self):
        for mock_id in self.mock_ids:
            request = urllib.request.Request(
                f'http://{TouchstoneConfig.instance().config["host"]}:{self.exposed_port()}/__admin/mappings/{mock_id}',
                method='DELETE')
            urllib.request.urlopen(request)

    def mock_get(self, endpoint: str, response: str, response_status: int = 200,
                 response_headers: Dict = {'Content-Type': 'application/json'}):
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

    def mock_post(self, endpoint: str, response: str, response_status: int = 200,
                  response_headers: Dict = {'Content-Type': 'application/json'}):
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

    def mock_put(self, endpoint: str, response: str, response_status: int = 200,
                 response_headers: Dict = {'Content-Type': 'application/json'}):
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

    def mock_delete(self, endpoint: str, response: str, response_status: int = 200,
                    response_headers: Dict = {'Content-Type': 'application/json'}):
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

    def __submit_mock(self, mock: Dict):
        data = json.dumps(mock).encode('utf8')
        request = urllib.request.Request(
            f'http://{TouchstoneConfig.instance().config["host"]}:{self.exposed_port()}/__admin/mappings', data=data,
            headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        self.mock_ids.append(json.loads(response)['id'])
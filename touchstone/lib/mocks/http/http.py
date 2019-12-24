import http
import http.client
import urllib.error
import urllib.parse
import urllib.request

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.http.http_exercise import HttpExercise
from touchstone.lib.mocks.http.http_setup import HttpSetup
from touchstone.lib.mocks.http.http_verify import HttpVerify
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.mock_case import Verify, Exercise, Setup


class Http(Mock):
    def __init__(self, mock_config: dict):
        super().__init__(mock_config)
        self.__container_name: str = None
        self.__setup = HttpSetup(self.default_url())
        self.__exercise = HttpExercise()
        self.__verify = HttpVerify(self.default_url())

    @staticmethod
    def name() -> str:
        return 'http'

    @staticmethod
    def pretty_name() -> str:
        return 'HTTP'

    def default_port(self) -> int:
        return 8081

    def default_url(self) -> str:
        return 'http://' + super().default_url()

    def ui_endpoint(self) -> str:
        return '/__admin'

    def is_healthy(self) -> bool:
        try:
            response = urllib.request.urlopen(self.ui_url()).read()
            return False if response is None else True
        except (urllib.error.URLError, http.client.RemoteDisconnected):
            return False

    def start(self):
        self.__container_name = DockerManager.instance().run_image('rodolpheche/wiremock:2.25.1-alpine',
                                                                   [(self.default_port(), 8080)])

    def stop(self):
        DockerManager.instance().stop_container(self.__container_name)

    def setup(self) -> Setup:
        return self.__setup

    def exercise(self) -> Exercise:
        return self.__exercise

    def verify(self) -> Verify:
        return self.__verify

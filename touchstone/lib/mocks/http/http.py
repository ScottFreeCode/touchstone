import http
import http.client
import urllib.error
import urllib.parse
import urllib.request

from lib.configs.touchstone_config import TouchstoneConfig
from lib.docker_manager import DockerManager
from lib.mocks.http.http_exercise import HttpExercise
from lib.mocks.http.http_setup import HttpSetup
from lib.mocks.http.http_verify import HttpVerify
from lib.mocks.mock import Mock
from lib.mocks.mock_case import Verify, Exercise, Setup


class Http(Mock):
    def __init__(self, mock_config: dict):
        super().__init__(mock_config)
        self.__setup = HttpSetup(self.exposed_port())
        self.__exercise = HttpExercise(self.exposed_port())
        self.__verify = HttpVerify(self.exposed_port())

    @staticmethod
    def name() -> str:
        return 'http'

    @staticmethod
    def pretty_name() -> str:
        return 'HTTP'

    def default_exposed_port(self) -> int:
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

    def setup(self) -> Setup:
        return self.__setup

    def exercise(self) -> Exercise:
        return self.__exercise

    def verify(self) -> Verify:
        return self.__verify
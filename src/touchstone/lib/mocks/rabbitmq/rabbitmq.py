import http
import http.client
import urllib.error
import urllib.request
from typing import Optional

import pika

from touchstone.lib.docker_manager import DockerManager
from touchstone.lib.mocks.mock import Mock
from touchstone.lib.mocks.rabbitmq.rabbitmq_setup import RabbitmqSetup
from touchstone.lib.mocks.rabbitmq.rabbitmq_verify import RabbitmqVerify
from touchstone.lib.mocks.rabbitmq.rmq_context import RmqContext


class Rabbitmq(Mock):
    def __init__(self, default_host: str, docker_manager: DockerManager):
        super().__init__(default_host)
        self.setup: RabbitmqSetup = None
        self.verify: RabbitmqVerify = None
        self.__docker_manager = docker_manager
        self.__container_name: Optional[str] = None

    @staticmethod
    def name() -> str:
        return 'rabbitmq'

    @staticmethod
    def pretty_name() -> str:
        return 'Rabbit MQ'

    def default_config(self) -> dict:
        return {
            'durable': False
        }

    def default_port(self) -> int:
        return 5672

    def ui_port(self) -> int:
        return 15672

    def is_healthy(self) -> bool:
        try:
            response = urllib.request.urlopen(f'{self.ui_url()}').read()
            return response is not None
        except (urllib.error.URLError, http.client.RemoteDisconnected):
            return False

    def start(self):
        self.__container_name = self.__docker_manager.run_image('rabbitmq:3.7.22-management-alpine',
                                                                [(self.default_port(), 5672),
                                                                 (self.ui_port(), 15672)])

    def initialize(self):
        connection_params = pika.ConnectionParameters(
            host=self.default_host(),
            port=self.default_port(),
            credentials=pika.PlainCredentials('guest', 'guest'),
            heartbeat=0
        )
        connection = pika.BlockingConnection(connection_params)
        rmq_context = RmqContext()
        channel = connection.channel()
        self.setup = RabbitmqSetup(channel, connection_params, rmq_context, self.config['durable'])
        self.verify = RabbitmqVerify(channel, rmq_context)

    def stop(self):
        if self.__container_name:
            self.setup.stop_listening()
            self.__docker_manager.stop_container(self.__container_name)

    def load_defaults(self, defaults: dict):
        self.setup.load_defaults(defaults)

    def reset(self):
        self.setup.reset()

import unittest
from unittest import TestCase
from unittest.mock import Mock

from touchstone.lib import exceptions
from touchstone.lib.networking.docker_network import DockerNetwork
from touchstone.lib.services.networked_service import NetworkedService


class TestService(TestCase):
    def setUp(self) -> None:
        self.mock_tests = Mock()
        self.mock_docker_manager = Mock()
        self.mock_blocking_health_check = Mock()

    def test_start_dockerfileNotSet_exceptionRaised(self):
        # Given
        service = NetworkedService('', self.mock_tests, None, None, None, self.mock_docker_manager, 0, '', None,
                                   DockerNetwork(), self.mock_blocking_health_check)

        # Then
        self.assertRaises(exceptions.ServiceException, service.start, [])

    def test_stop_serviceIsRunning_serviceStops(self):
        service = NetworkedService('', self.mock_tests, '', None, None, self.mock_docker_manager, 0, '', None,
                                   DockerNetwork(), self.mock_blocking_health_check)

        # When
        service.start([])
        service.stop()

        # Then
        self.mock_docker_manager.stop_container.assert_called_once()
        self.assertFalse(service.is_running())


if __name__ == '__main__':
    unittest.main()

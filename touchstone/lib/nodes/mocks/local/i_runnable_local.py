from abc import ABC

from touchstone.lib.health_checks.i_health_checkable import IHealthCheckable
from touchstone.lib.nodes.mocks.behaviors.i_behavior import IBehavior
from touchstone.lib.nodes.mocks.i_runnable import IRunnable


class IRunnableLocal(ABC, IRunnable, IHealthCheckable):
    def get_behavior(self) -> IBehavior:
        pass

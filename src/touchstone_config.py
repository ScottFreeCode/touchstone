import sys
from typing import Dict


class TouchstoneConfig:
    __instance = None

    @staticmethod
    def instance():
        if TouchstoneConfig.__instance is None:
            TouchstoneConfig()
        return TouchstoneConfig.__instance

    def __init__(self):
        TouchstoneConfig.__instance = self
        self.config = {
            'root': None,
            'dev': False,
            'host': 'localhost'
        }

        if 'dev' in sys.argv:
            self.config['dev'] = True

    def set_root(self, root):
        self.config['root'] = root

    def merge(self, other: Dict):
        self.config = dict(list(self.config.items()) + list(other.items()))
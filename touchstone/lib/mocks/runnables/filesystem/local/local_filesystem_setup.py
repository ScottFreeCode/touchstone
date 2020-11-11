import os
import shutil
import subprocess

from touchstone.lib.mocks.runnables.filesystem.i_filesystem_behavior import IFilesystemSetup


class LocalFilesystemSetup(IFilesystemSetup):
    def __init__(self, files_path: str, base_files_path: str):
        self.__files_path = files_path
        self.__base_files_path = base_files_path

    def reset(self):
        self.delete_defaults()
        shutil.copytree(self.__base_files_path, self.__files_path)
        if os.name is not 'nt':
            subprocess.run(['chmod', '-R', '777', self.__files_path])

    def delete_defaults(self):
        shutil.rmtree(self.__files_path)

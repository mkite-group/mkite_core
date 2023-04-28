import os
import shutil
from datetime import datetime
from abc import ABC, abstractmethod


class Runnable(ABC):
    @abstractmethod
    def run(self):
        """Runs the job"""

    def pwd(self):
        return os.path.abspath(".")

    @property
    def timestamp(self):
        tsec = int(datetime.timestamp(datetime.now()))
        return str(tsec)

    def to_folder(self, src: os.PathLike, dst: os.PathLike):
        _smart_copy(src, dst)
        os.chdir(dst)


def _smart_copy(src, dst):
    for f in os.listdir(src):
        src_path = os.path.join(src, f)

        if os.path.abspath(src_path) == os.path.abspath(dst):
            continue

        if os.path.isdir(src_path):
            shutil.copytree(src_path, os.path.join(dst, f))

        else:
            shutil.copy2(src_path, dst)

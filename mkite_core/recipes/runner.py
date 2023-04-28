import subprocess
from abc import ABC, abstractmethod
from .settings import EnvSettings


class BaseRunner(ABC):
    def __init__(
        self,
        settings: EnvSettings,
        stdout: str = "stdout.out",
        stderr: str = "stderr.out",
    ):
        self.settings = settings
        self.stdout = stdout
        self.stderr = stderr

    @property
    @abstractmethod
    def cmd(self):
        """Command used to execute the runner"""

    def run(self):
        with open(self.stderr, "w", buffering=1) as err:
            return subprocess.run(self.cmd, stdout=subprocess.PIPE, stderr=err)

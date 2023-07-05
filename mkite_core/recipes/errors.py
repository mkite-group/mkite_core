import json
import os
import shutil
from abc import ABC
from abc import abstractmethod

from mkite_core.models import JobInfo
from mkite_core.models import RunStatsInfo


class BaseErrorHandler(ABC):
    """Base class to handle errors from the calculations. Error handlers
    implement what to do when the recipe failed. In this case, the error
    handler parses whatever happened with the recipe and re-adds it to
    the engine to attempt restarting it.
    """

    def __init__(self, info: JobInfo, workdir: os.PathLike):
        self.info = info
        self.workdir = workdir

    def get_path(self, filename: str):
        """Join the workdir to the given `filename`."""
        return os.path.join(self.workdir, filename)

    def set_status(self, info: JobInfo, status: str) -> JobInfo:
        """Updates the status of the JobInfo"""
        info.job["status"] = status
        return info

    def delete_scratch(self):
        shutil.rmtree(self.workdir)

    @abstractmethod
    def handle(self) -> JobInfo:
        """Method that handles the error given a workdir"""

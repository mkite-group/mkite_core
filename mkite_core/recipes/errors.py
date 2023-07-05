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

    def __init__(self, workdir: os.PathLike, delete: bool = False):
        self.workdir = workdir
        self.delete = delete
        self.info = self.get_info()
        self.runstats = self.get_runstats()

    def get_path(self, filename: str):
        """Join the workdir to the given `filename`."""
        return os.path.join(self.workdir, filename)

    def get_info(self) -> JobInfo:
        path = self.get_path(JobInfo.file_name())
        return JobInfo.from_json(path)

    def get_runstats(self) -> RunStatsInfo:
        path = self.get_path(RunStatsInfo.file_name())
        if os.path.exists(path):
            return RunStatsInfo.from_json(path)

        return None

    def set_status(self, info: JobInfo, status: str) -> JobInfo:
        """Updates the status of the JobInfo"""
        info.job["status"] = status
        return info

    def delete_workdir(self):
        shutil.rmtree(self.workdir)

    @abstractmethod
    def handle(self) -> JobInfo:
        """Method that handles the error given a workdir"""

import os
import re
import json
from abc import ABC, abstractmethod

from mkite_core.models import JobInfo, JobResults, RunStatsInfo


class ParseError(Exception):
    pass


class BaseParser(ABC):
    """Base class to postprocess results from the calculations. Each
    recipe should implement the methods of which files to open and what
    information to extract from them. The results have to be saved in
    a plain JSON file, but do not necessarily have to be compatible with
    the models at `mkite`. This means the user knows how to interact
    with `mkite` if needed, but doesn't have to setup a database to
    parse and analyze the results.
    """

    def __init__(self, workdir: os.PathLike):
        self.workdir = workdir
        self.results: dict = {}

    @abstractmethod
    def parse(self) -> JobResults:
        """Functions that will be run to parse the results of the recipe"""

    def to_json(self, obj, filename: os.PathLike):
        with open(filename, "w") as f:
            json.dump(obj, f)

    def load_json(self, filename: os.PathLike):
        with open(filename, "r") as f:
            return json.load(f)

    def get_path(self, filename: str):
        """Join the workdir to the given `filename`."""
        return os.path.join(self.workdir, filename)

    def get_runstats(self):
        import socket

        info = {
            "host": socket.gethostname(),
            "cluster": socket.getfqdn(),
        }

        path = os.path.join(self.workdir, RunStatsInfo.file_name())

        # sometimes, jobs are located inside folders created by the recipe for isolation
        # Hence, we need to check whether the parent_path has a runstats.json file too
        parent_path = os.path.join(self.workdir, "..", RunStatsInfo.file_name())

        if os.path.exists(path):
            stats = self.load_json(path)
        elif os.path.exists(parent_path):
            stats = self.load_json(parent_path)
        else:
            return info

        gpus = stats.get("gpus")
        if gpus is not None:
            info["ngpus"] = int(gpus)

        tasks = stats.get("ntasks")
        if tasks is not None:
            info["ncores"] = int(tasks)

        return info

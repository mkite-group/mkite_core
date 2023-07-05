from datetime import datetime
from typing import List
from typing import Optional
from typing import Union

from .base import BaseInfo
from .base import NodeResults


class JobInfo(BaseInfo):
    job: dict
    recipe: dict
    options: dict
    inputs: List[dict]
    workdir: Optional[str] = None

    @property
    def uuid(self):
        if "uuid" not in self.job:
            self.job["uuid"] = self.create_uuid()

        return str(self.job["uuid"])

    @property
    def uuid_short(self):
        return self.uuid[:8]

    @property
    def id(self):
        if "uuid" in self.job:
            return self.uuid

        if "id" in self.job:
            return f"id_{self.job['id']}"

        raise ValueError("No identifier for the job")

    @property
    def folder_prefix(self):
        recipe_name = self.recipe.get("name", "unnamed")
        return f"{recipe_name}_{self.uuid_short}"

    @property
    def folder_name(self):
        prefix = self.folder_prefix
        timestamp = int(datetime.timestamp(datetime.now()))
        return f"{prefix}_{timestamp}"

    @classmethod
    def from_job(cls, job: "Job") -> "JobInfo":
        def get_inputs(job: "Job"):
            inputs = []
            for node in job.inputs.all():
                data = node.get_data()
                inputs.append(data)

            return inputs

        return cls(
            job=job.as_dict(),
            recipe=job.recipe.as_dict(),
            options=job.options,
            inputs=get_inputs(job),
        )

    @staticmethod
    def file_name():
        return "jobinfo.json"


class RunStatsInfo(BaseInfo):
    host: str
    cluster: str
    duration: Union[float, str]
    ncores: int
    ngpus: int
    pkgversion: str = None

    @staticmethod
    def file_name():
        return "runstats.json"

    def __add__(self, other):
        args = other.as_dict()
        args["duration"] = self.duration + other.duration
        return self.__class__(**args)


class JobResults(BaseInfo):
    """Encodes the results of a job into an object that can be converted
    to a Job in ORM without any problem. The benefit of having an extra object
    to deal with this is that the interface between ORM/job submission engine
    does not get bloated with methods.

    Parameters:
        runstats: dictionary containing the description of RunStats, such as
            host name, wall time, number of cores/GPUs etc.
        nodes: list of ChemNodes containing all the information necessary to
            create each ChemNode. This special representation includes a key
            in each ChemNode dictionary called `calcnodes`, which should be a
            list of dictionaries. If the key `calcnodes` is not found in the
            ChemNode dictionary, no calcs associated to the ChemNode are created.
    """

    job: dict
    runstats: RunStatsInfo = {}
    nodes: List[NodeResults] = []
    workdir: Optional[str] = None

    @property
    def uuid(self):
        if "uuid" not in self.job:
            self.job["uuid"] = self.create_uuid()

        return str(self.job["uuid"])

    @property
    def uuid_short(self):
        return self.uuid[:8]

    @property
    def id(self):
        if "uuid" in self.job:
            return self.uuid

        if "id" in self.job:
            return f"id_{self.job['id']}"

        raise ValueError("No identifier for the job")

    @staticmethod
    def file_name():
        return "jobresults.json"

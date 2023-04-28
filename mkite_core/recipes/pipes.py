import shutil
from mkite_core.models import JobResults, JobInfo

from .base import Runnable


class JobPipe(Runnable):
    """Class that connects results from the previous job to the
    input of the next job"""

    def __init__(self, info: JobInfo, results: JobResults):
        self.info = info
        self.results = results

    def run(self) -> JobInfo:
        new_info = self.modify_info()
        return new_info

    def modify_info(self) -> JobInfo:
        return self.info


class SaveResultsPipe(JobPipe):
    def run(self) -> JobInfo:
        self.results.to_json(JobResults.file_name())
        return self.info


class CopyWorkdirPipe(JobPipe):
    def run(self) -> JobInfo:
        if getattr(self.results, "workdir", None) is None:
            return self.info

        src = self.results.workdir
        dst = src + ".copy"
        shutil.copytree(src, dst)
        self.info.workdir = dst
        return self.info

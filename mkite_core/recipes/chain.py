import os
from typing import List, Union

from mkite_core.models import JobResults, JobInfo

from .base import Runnable
from .recipe import BaseRecipe
from .pipes import JobPipe


class RecipeChain(Runnable):
    JOBS: List[Union[BaseRecipe, JobPipe]]

    def __init__(
        self,
        info: JobInfo,
        settings_path: os.PathLike = None,
    ):
        self.info = info
        self.settings_path = settings_path

    def run(self) -> JobResults:
        info = self.info
        results = None

        total_duration = 0
        for jcls in self.JOBS:
            if issubclass(jcls, BaseRecipe):
                job = jcls(info, settings_path=self.settings_path)
                results = job.run()
                total_duration += results.runstats.get("duration", 0)

            results.runstats["duration"] = round(total_duration, 6)
            if issubclass(jcls, JobPipe):
                job = jcls(info, results)
                info = job.run()

        return results

    def handle_errors(self, **kwargs) -> JobInfo:
        # use handle_errors from the first recipe
        jcls = [j for j in self.JOBS if issubclass(j, BaseRecipe)][0]
        job = jcls(self.info, settings_path=self.settings_path)
        return job.handle_errors(**kwargs)

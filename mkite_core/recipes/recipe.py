import json
import os
import shutil
import socket
import subprocess
import tempfile
import traceback
from abc import abstractmethod
from typing import List

from mkite_core.models import JobInfo, JobResults, RunStatsInfo, Status
from pkg_resources import get_distribution

from .base import Runnable
from .errors import BaseErrorHandler
from .options import BaseOptions
from .parser import BaseParser
from .runner import BaseRunner
from .settings import EnvSettings


class RecipeError(Exception):
    pass


class PythonRecipe(Runnable):
    """Base recipe for any python script that does not have to be
    run by an external program. This is useful when running several
    scripts to manipulate structures, featurize, or perform data
    analysis. Does not use `PARSER_CLS` nor `RUNNER_CLS` to parse
    or run the recipe. Instead, uses the implemented `run` method.
    """

    _PACKAGE_NAME: str = None
    _METHOD: str = None

    SETTINGS_CLS: EnvSettings = EnvSettings
    OPTIONS_CLS: BaseOptions = None
    ERROR_CLS: BaseErrorHandler = None

    @abstractmethod
    def run(self) -> JobResults:
        """Runs the script"""

    def __init__(
        self, info: JobInfo, settings_path: os.PathLike = None, workdir: str = None
    ):
        self.info = info
        self.settings = self._load_settings(settings_path)
        self.workdir = workdir

    def _load_settings(self, path: os.PathLike = None):
        """Loads the settings relevant to the recipe using the
        SETTINGS_CLS defined in the recipe class and the `path`
        provided as an argument.
        """
        if path is not None and os.path.exists(path):
            return self.SETTINGS_CLS.from_file(path)

        return self.SETTINGS_CLS()

    @classmethod
    def from_json(cls, filename: os.PathLike):
        info = JobInfo.from_json(filename)
        return cls(info)

    def get_options(self):
        """Builds an options dictionary for recipes"""
        options = self.OPTIONS_CLS().model_dump()
        options = BaseOptions.dict_update(options, self.info.options)
        return options

    def get_inputs(self):
        return self.info.inputs

    def get_done_job(self) -> dict:
        job = {k: self.info.job[k] for k in ["id", "uuid"] if k in self.info.job}
        job["status"] = "D"

        # required to serialize the options coming
        # from a yaml or anything that generates
        # an OrderedDict
        opts = self.get_options()
        job["options"] = json.loads(json.dumps(opts))
        return job

    def get_run_stats(self, duration: float, num_cores: bool = False) -> RunStatsInfo:
        ncores = os.cpu_count() if num_cores else 1
        host = socket.gethostname()
        cluster = socket.gethostbyname(host)

        return RunStatsInfo(
            host=host[:64],
            cluster=cluster[:64],
            duration=round(duration, 6),
            ncores=ncores,
            ngpus=0,
            pkgversion=self.get_version(),
        )

    def get_version(self):
        module_name = self.__module__.split(".")[0]
        return str(get_distribution(module_name))

    def handle_errors(self) -> JobInfo:
        """Handle errors that may have happened with the execution
        of the recipe. After handling the errors, the recipe
        returns the relevant information to restart (or not)
        the job.
        """
        handler = self.ERROR_CLS(".", delete=False)
        return handler.handle()


class BaseRecipe(PythonRecipe):
    """Base class to run any recipe job with external codes.
    Helps to wrap the jobs around the submission engine,
    the defaults, and data extraction.
    """

    _PACKAGE_NAME: str = None
    _METHOD: str = None
    SETTINGS_CLS: EnvSettings = EnvSettings
    OPTIONS_CLS: BaseOptions = None
    PARSER_CLS: BaseParser = None
    RUNNER_CLS: BaseRunner = None
    ERROR_CLS: BaseErrorHandler = None

    @abstractmethod
    def setup(self, workdir):
        """Sets up the workdir to start the calculations of the recipe"""

    def run_job(self):
        runner = self.RUNNER_CLS(self.settings)
        return runner.run()

    def postprocess(self, calcdir) -> JobResults:
        parser = self.PARSER_CLS(calcdir)
        results = parser.parse()

        results = self.propagate_key(results, key="attributes")
        results.job = self.get_done_job()

        results.to_json(os.path.join(calcdir, JobResults.file_name()))
        return results

    def propagate_key(self, results: JobResults, key="attributes"):
        """Propagates a key from the input to the output. By default, joins
        all the keys from all inputs and places then into the output. Useful
        when propagating information such as `attributes`"""

        attrs = {}
        for inp in self.info.inputs:
            attrs = {**attrs, **inp.get(key, {})}

        for node_results in results.nodes:
            node_results.chemnode[key] = {**attrs, **node_results.chemnode.get(key, {})}

        return results

    def get_scratch(self):
        return os.path.abspath(self.settings.SCRATCH_DIR)

    def get_workdir(self):
        name = os.path.abspath(f"./{self.__class__.__name__}_{self.timestamp}")

        if getattr(self.info, "workdir", None) is not None:
            src = os.path.abspath(self.info.workdir)
            shutil.move(src, name)

        return name

    def run(self) -> JobResults:
        basedir = self.pwd()
        workdir = self.get_workdir()
        self.setup(workdir)
        with tempfile.TemporaryDirectory(
            prefix=f"{self.info.folder_name}_",
            dir=self.get_scratch(),
        ) as tempdir:
            try:
                self.to_folder(workdir, tempdir)
                self.run_job()
                results = self.postprocess(tempdir)

                if hasattr(results, "workdir"):
                    results.workdir = workdir

            except Exception as e:
                traceback.print_exc()
                results = None

            finally:
                self.to_folder(tempdir, workdir)
                os.chdir(basedir)
                return results

    def get_existing_scratch(self, abspath: bool = True) -> List[str]:
        scratch = self.get_scratch()
        job_folders = [
            f for f in os.listdir(scratch) if f.startswith(self.info.folder_prefix)
        ]
        if not abspath:
            return job_folders

        return [os.path.join(scratch, f) for f in job_folders]

    def handle_errors(self, delete_scratch: bool = False) -> JobInfo:
        """Handle errors that may have happened with the execution
        of the recipe. After handling the errors, the recipe
        returns the relevant information to restart (or not)
        the job.
        """
        tmp_folders = self.get_existing_scratch(abspath=True)
        job_folders = [
            f for f in os.listdir(".") if f.startswith(self.__class__.__name__)
        ]

        if len(tmp_folders) > 0:
            folder = sorted(tmp_folders)[-1]

        elif len(job_folders) > 0:
            folder = sorted(job_folders)[-1]

        else:
            # could not find any information about temporary
            # files for the job. Return the existing job as
            # an error
            info = self.info.copy()
            info.job["status"] = Status.ERROR.value
            return info

        handler = self.ERROR_CLS(self.info, folder)
        info = handler.handle()

        if delete_scratch:
            handler.delete_scratch()

        return info

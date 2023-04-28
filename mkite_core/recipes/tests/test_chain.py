import os
import json
import unittest as ut
from pathlib import Path
from unittest.mock import patch, MagicMock
from pkg_resources import resource_filename

from mkite_core.models import JobInfo, JobResults
from mkite_core.tests.tempdirs import run_in_tempdir
from mkite_core.recipes import BaseRecipe, RecipeChain, BaseRunner, BaseParser
from mkite_core.recipes.pipes import JobPipe


INFO_FILE = resource_filename("mkite_core.tests.files", "jobinfo.json")
SETTINGS_FILE = resource_filename("mkite_core.tests.files", "settings.yaml")


ENVIRONMENT = {
    "SCRATCH_DIR": ".",
}


class MockRecipe(BaseRecipe):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.PARSER_CLS = MagicMock()
        self.RUNNER_CLS = MagicMock()
        self.OPTIONS_CLS = MagicMock()
        self.OPTIONS_CLS.dict.return_value = {}

    def get_options(self):
        return {}

    def setup(self, workdir):
        if not os.path.exists(workdir):
            os.mkdir(workdir)

    def run(self):
        runstats = {
            "host": "test",
            "cluster": "test_cluster",
            "duration": 5,
            "ncores": 1,
            "ngpus": 0,
        }
        results = JobResults(
            job={"id": 1},
            runstats=runstats,
            nodes=[],
        )
        return results


class MockJobPipe(JobPipe):
    pass


class TestChain(ut.TestCase):
    def setUp(self):
        self.info = JobInfo.from_json(INFO_FILE)

    @run_in_tempdir
    def test_run(self):
        jobs = [
            MockRecipe,
            MockJobPipe,
            MockRecipe,
        ]
        chain = RecipeChain(self.info)
        chain.JOBS = jobs
        results = chain.run()

        duration = results.runstats["duration"]
        self.assertEqual(duration, 10)

import json
import unittest as ut
from datetime import datetime
from freezegun import freeze_time
from pkg_resources import resource_filename

from mkite_core.tests.tempdirs import run_in_tempdir
from mkite_core.models.jobs import JobInfo, RunStatsInfo


INFO_FILE = resource_filename("mkite_core.tests.files", "jobinfo.json")
RESULTS_FILE = resource_filename("mkite_core.tests.files", "jobresults.json")

with open(INFO_FILE, "r") as f:
    INFO = json.load(f)


class TestJobInfo(ut.TestCase):
    def setUp(self):
        self.data = INFO
        self.info = JobInfo.from_json(INFO_FILE)

    def test_from_json(self):
        self.assertEqual(self.info.job, self.data["job"])
        self.assertEqual(self.info.recipe, self.data["recipe"])
        self.assertEqual(self.info.options, self.data["options"])
        self.assertEqual(self.info.inputs, self.data["inputs"])

    @run_in_tempdir
    def test_to_json(self):
        name = "test.json"
        self.info.to_json(name)
        new = JobInfo.from_json(name)

        self.assertEqual(self.info, new)

    def test_uuid(self):
        self.assertEqual(self.info.uuid_short, "7615c560")

    def test_name(self):
        with freeze_time("2022-07-26"):
            name = self.info.folder_name

        TIMESTAMP = 1658793600
        expected = f"test_recipe_7615c560_{TIMESTAMP}"

        self.assertEqual(name, expected)

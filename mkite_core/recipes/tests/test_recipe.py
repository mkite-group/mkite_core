import os
import json
import unittest as ut
from pathlib import Path
from unittest.mock import patch, MagicMock
from pkg_resources import resource_filename

from mkite_core.models import JobInfo
from mkite_core.tests.tempdirs import run_in_tempdir
from mkite_core.recipes.recipe import BaseRecipe, BaseOptions


INFO_FILE = resource_filename("mkite_core.tests.files", "jobinfo.json")
INFO = JobInfo.from_json(INFO_FILE)
SETTINGS_FILE = resource_filename("mkite_core.tests.files", "settings.yaml")


ENVIRONMENT = {
    "SCRATCH_DIR": ".",
}


class MockRecipe(BaseRecipe):
    def setup(self, workdir):
        if not os.path.exists(workdir):
            os.mkdir(workdir)


class MockOptions(BaseOptions):
    def dict(self):
        return {}


class TestRecipe(ut.TestCase):
    @patch.dict(os.environ, ENVIRONMENT)
    def setUp(self):
        self.recipe = MockRecipe(INFO)
        self.recipe.PARSER_CLS = MagicMock()
        self.recipe.RUNNER_CLS = MagicMock()
        self.recipe.OPTIONS_CLS = MockOptions

    @patch.dict(os.environ, ENVIRONMENT)
    def test_load_settings(self):
        setts = self.recipe._load_settings()
        self.assertEqual(str(setts.SCRATCH_DIR), ".")

        setts = self.recipe._load_settings(SETTINGS_FILE)
        self.assertEqual(str(setts.SCRATCH_DIR), "/tmp")

    def test_run_job(self):
        result = self.recipe.run_job()
        mock_obj = self.recipe.RUNNER_CLS
        self.assertTrue(mock_obj.called)
        self.assertTrue(mock_obj.return_value.run.called)

    def test_postprocess(self):
        result = self.recipe.postprocess(".")
        mock_cls = self.recipe.PARSER_CLS
        self.assertTrue(mock_cls.called)

        mock_obj = mock_cls.return_value
        self.assertTrue(mock_obj.parse.called)

    def test_options(self):
        self.assertEqual(self.recipe.get_options(), INFO.options)

    def test_inputs(self):
        self.assertEqual(self.recipe.get_inputs(), INFO.inputs)

    def test_scratch(self):
        d = self.recipe.get_scratch()
        expected = os.path.abspath(ENVIRONMENT["SCRATCH_DIR"])

        self.assertEqual(d, expected)

    def test_from_json(self):
        recipe = MockRecipe.from_json(INFO_FILE)
        self.assertIsInstance(recipe.info, JobInfo)

    @run_in_tempdir
    @patch("tempfile.TemporaryDirectory")
    def test_run(self, mock_tempfile):
        self.recipe.to_folder = MagicMock()
        self.recipe.run()

        self.assertTrue(mock_tempfile.called)

        mock_cls = self.recipe.RUNNER_CLS
        self.assertTrue(mock_cls.called)

        mock_cls = self.recipe.PARSER_CLS
        self.assertTrue(mock_cls.called)

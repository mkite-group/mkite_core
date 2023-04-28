import os
import unittest as ut
from unittest.mock import patch

from mkite_core.tests.tempdirs import run_in_tempdir
from mkite_core.recipes.runner import BaseRunner
from mkite_core.recipes.settings import EnvSettings


class MockRunner(BaseRunner):
    @property
    def cmd(self):
        return ["echo", "test"]


class TestRunner(ut.TestCase):
    def setUp(self):
        self.runner = MockRunner(settings=EnvSettings())

    @run_in_tempdir
    def test_run(self):
        results = self.runner.run()
        out = results.stdout.decode()

        self.assertEqual(out, "test\n")
        self.assertTrue(os.path.exists("./stderr.out"))

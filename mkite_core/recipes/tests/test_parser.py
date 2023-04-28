import os
import json
import unittest as ut
from unittest.mock import patch

from mkite_core.tests.tempdirs import run_in_tempdir
from mkite_core.recipes.parser import BaseParser


class MockParser(BaseParser):
    def parse(self):
        return {}


class TestParser(ut.TestCase):
    def setUp(self):
        self.parser = MockParser(workdir=".")

    def test_path(self):
        name = "test_file"
        path = self.parser.get_path(name)
        self.assertEqual(path, f"./{name}")

    @run_in_tempdir
    def test_json(self):
        test = {"test": 1}
        name = "test_file.json"

        self.parser.to_json(test, name)

        with open(name, "r") as f:
            data = json.load(f)

        self.assertEqual(data, test)

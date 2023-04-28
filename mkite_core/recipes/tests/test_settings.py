import os
import unittest as ut
from unittest.mock import patch
from pkg_resources import resource_filename

from mkite_core.recipes.settings import EnvSettings

SETTINGS_FILE = resource_filename("mkite_core.tests.files", "settings.yaml")

ENVIRONMENT = {
    "SCRATCH_DIR": "/bin",
}


class TestRecipes(ut.TestCase):
    @patch.dict(os.environ, ENVIRONMENT)
    def setUp(self):
        self.settings = EnvSettings()

    def test_scratch(self):
        self.assertTrue(hasattr(self.settings, "SCRATCH_DIR"))
        self.assertEqual(str(self.settings.SCRATCH_DIR), "/bin")

    def test_from_file(self):
        settings = EnvSettings.from_file(SETTINGS_FILE)
        self.assertEqual(str(settings.SCRATCH_DIR), "/tmp")

import os
import unittest as ut
from pathlib import Path
from unittest.mock import patch, MagicMock

from mkite_core.tests.tempdirs import run_in_tempdir
from mkite_core.recipes.base import Runnable, _smart_copy


class MockRunnable(Runnable):
    def run(self):
        return True


class TestRunnable(ut.TestCase):
    def setUp(self):
        self.run = MockRunnable()

    def test_pwd(self):
        testdir = "/"
        os.chdir(testdir)
        self.assertEqual(self.run.pwd(), testdir)

    @patch("mkite_core.recipes.base._smart_copy")
    def test_to_folder(self, mock_copy):
        src, dst = ".", "/tmp"
        self.run.to_folder(src, dst)
        self.assertTrue(self.run.pwd(), dst)
        self.assertTrue(mock_copy.called)


class TestCopy(ut.TestCase):
    def setUp(self):
        self.src = "src"
        self.dst = "dst"
        self.folder1 = os.path.join(self.src, "folder1")
        self.test1 = Path(os.path.join(self.src, "test1"))
        self.test2 = Path(os.path.join(self.src, "test2"))

    def prepare_dirs(self):
        os.mkdir(self.src)
        os.mkdir(self.dst)
        os.mkdir(self.folder1)
        self.test1.touch()
        self.test2.touch()

    @run_in_tempdir
    def test_copy(self):
        self.prepare_dirs()
        _smart_copy(self.src, self.dst)
        files = os.listdir(self.dst)
        self.assertTrue("test1" in files)
        self.assertTrue("test2" in files)
        self.assertTrue("folder1" in files)
        self.assertTrue(os.path.isdir(os.path.join(self.dst, "folder1")))

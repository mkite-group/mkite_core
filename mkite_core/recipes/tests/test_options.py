import unittest as ut
from mkite_core.recipes.options import BaseOptions


class MockOpts(BaseOptions):
    char: str


class TestOptions(ut.TestCase):
    def test_update(self):
        original = {
            "a": 1,
            "b": 2,
            "c": {
                "c1": 4,
                "c2": 5,
            },
        }

        update = {"b": 6, "c": {"c2": 6, "c3": 7}}

        new = BaseOptions.dict_update(original, update)

        expected = {
            "a": 1,
            "b": 6,
            "c": {
                "c1": 4,
                "c2": 6,
                "c3": 7,
            },
        }

        self.assertEqual(new, expected)

    def test_dict(self):
        opts = MockOpts(char="a")
        self.assertIsInstance(opts.model_dump(), dict)

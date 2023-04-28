import unittest as ut
from copy import deepcopy
from pkg_resources import resource_filename

from ase import Atoms
from pymatgen.core import Structure

from mkite_core.models.structs import CrystalInfo


TEST_CRYSTAL = resource_filename("mkite_core.tests.files.models", "crystal.json")


class TestCrystalInfo(ut.TestCase):
    def setUp(self):
        self.crystal = CrystalInfo.from_json(TEST_CRYSTAL)

    def get_pymatgen(self):
        return Structure.from_dict(
            {
                "@module": "pymatgen.core.structure",
                "@class": "Structure",
                "charge": 0,
                "lattice": {
                    "matrix": [[0.0, 2.73, 2.73], [2.73, 0.0, 2.73], [2.73, 2.73, 0.0]],
                    "pbc": (True, True, True),
                    "a": 3.8608030252785492,
                    "b": 3.8608030252785492,
                    "c": 3.8608030252785492,
                    "alpha": 60.0,
                    "beta": 60.0,
                    "gamma": 60.0,
                    "volume": 40.692834,
                },
                "sites": [
                    {
                        "species": [{"element": "Si", "occu": 1}],
                        "abc": [0.0, 0.0, 0.0],
                        "xyz": [0.0, 0.0, 0.0],
                        "label": "Si",
                        "properties": {},
                    },
                    {
                        "species": [{"element": "Si", "occu": 1}],
                        "abc": [0.25, 0.25, 0.25],
                        "xyz": [1.365, 1.365, 1.365],
                        "label": "Si",
                        "properties": {},
                    },
                ],
            }
        )

    def get_ase(self):
        return Atoms.fromdict(
            {
                "numbers": [14, 14],
                "positions": [[0.0, 0.0, 0.0], [1.365, 1.365, 1.365]],
                "cell": [[0.0, 2.73, 2.73], [2.73, 0.0, 2.73], [2.73, 2.73, 0.0]],
                "pbc": [True, True, True],
            }
        )

    def test_as_pymatgen(self):
        structure = self.crystal.as_pymatgen()
        expected = self.get_pymatgen()

        self.assertEqual(structure, expected)

    def test_from_pymatgen(self):
        new = CrystalInfo.from_pymatgen(self.get_pymatgen())

        self.assertEqual(self.crystal, new)

    def test_from_ase(self):
        new = CrystalInfo.from_ase(self.get_ase())

        self.assertEqual(self.crystal, new)

    def test_as_ase(self):
        structure = self.crystal.as_ase()
        expected = self.get_ase()

        self.assertEqual(structure, expected)

    def test_inequality(self):
        self.assertNotEqual(self.crystal, ["test"])

        modified = deepcopy(self.crystal)
        modified.species = ["Si", "Al"]
        self.assertNotEqual(self.crystal, modified)

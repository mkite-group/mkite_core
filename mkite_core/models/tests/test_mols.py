import unittest as ut
from copy import deepcopy
from pkg_resources import resource_filename

from ase import Atoms
from pymatgen.core import Molecule
import rdkit.Chem.AllChem as Chem

from mkite_core.external.rdkit import RdkitInterface
from mkite_core.models.mols import MoleculeInfo, ConformerInfo


TEST_MOLECULE = resource_filename("mkite_core.tests.files.models", "molecule.json")
TEST_CONFORMER = resource_filename("mkite_core.tests.files.models", "conformer.json")


class TestMoleculeInfo(ut.TestCase):
    def setUp(self):
        self.molecule = MoleculeInfo.from_json(TEST_MOLECULE)

    def get_rdkit(self):
        interf = RdkitInterface.from_smiles(self.molecule.smiles)
        return interf.mol

    def test_as_rdkit(self):
        mol = self.molecule.as_rdkit()
        expected = self.get_rdkit()
        self.assertEqual(Chem.MolToSmiles(mol), Chem.MolToSmiles(expected))

    def test_from_rdkit(self):
        new = MoleculeInfo.from_rdkit(self.get_rdkit())
        self.assertEqual(self.molecule.inchikey, new.inchikey)

    def test_from_smiles(self):
        interf = RdkitInterface.from_smiles(self.molecule.smiles)
        new = MoleculeInfo.from_smiles(interf.smiles)
        self.assertEqual(self.molecule.inchikey, new.inchikey)

    def test_from_dict(self):
        new = MoleculeInfo.from_dict(self.molecule.as_dict())
        self.assertEqual(self.molecule, new)

    def test_inequality(self):
        self.assertNotEqual(self.molecule, ["test"])

        modified = deepcopy(self.molecule)
        modified.smiles = "c1ccccc1"
        self.assertNotEqual(self.molecule, modified)


class TestConformerInfo(ut.TestCase):
    def setUp(self):
        self.conformer = ConformerInfo.from_json(TEST_CONFORMER)

    def get_pymatgen(self):
        return Molecule.from_dict(
            {
                "@module": "pymatgen.core.structure",
                "@class": "Molecule",
                "charge": 0.0,
                "spin_multiplicity": 2,
                "sites": [
                    {
                        "name": "C",
                        "species": [{"element": "C", "occu": 1}],
                        "xyz": [2.3554, 0.8348, 0.6631],
                        "properties": {},
                    },
                    {
                        "name": "C",
                        "species": [{"element": "C", "occu": 1}],
                        "xyz": [1.5219, 0.0296, -0.32],
                        "properties": {},
                    },
                    {
                        "name": "N",
                        "species": [{"element": "N", "occu": 1}],
                        "xyz": [0.0, 0.0, 0.0],
                        "properties": {},
                    },
                    {
                        "name": "C",
                        "species": [{"element": "C", "occu": 1}],
                        "xyz": [-0.6558, -0.8654, -1.1138],
                        "properties": {},
                    },
                    {
                        "name": "C",
                        "species": [{"element": "C", "occu": 1}],
                        "xyz": [-2.1618, -1.0215, -0.9835],
                        "properties": {},
                    },
                    {
                        "name": "C",
                        "species": [{"element": "C", "occu": 1}],
                        "xyz": [-0.2675, -0.5998, 1.4101],
                        "properties": {},
                    },
                    {
                        "name": "C",
                        "species": [{"element": "C", "occu": 1}],
                        "xyz": [0.2466, -2.0174, 1.598],
                        "properties": {},
                    },
                    {
                        "name": "C",
                        "species": [{"element": "C", "occu": 1}],
                        "xyz": [-0.5986, 1.4355, 0.0238],
                        "properties": {},
                    },
                    {
                        "name": "C",
                        "species": [{"element": "C", "occu": 1}],
                        "xyz": [-0.4401, 2.2042, -1.2776],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [2.3048, 0.4326, 1.678],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [2.0679, 1.8889, 0.6861],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [3.4071, 0.7983, 0.3583],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [1.6352, 0.4327, -1.3317],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [1.8696, -1.0082, -0.3503],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [-0.4044, -0.4055, -2.0752],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [-0.1701, -1.8464, -1.0937],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [-2.4492, -1.521, -0.0549],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [-2.6861, -0.0647, -1.0469],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [-2.5322, -1.6425, -1.8067],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [-1.3484, -0.563, 1.5809],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [0.1933, 0.0706, 2.1429],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [0.014, -2.3532, 2.6146],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [1.3311, -2.0852, 1.4816],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [-0.2272, -2.7256, 0.9136],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [-1.6585, 1.3432, 0.2825],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [-0.1167, 1.9768, 0.8445],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [-0.8889, 3.1974, -1.1662],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [-0.9499, 1.7173, -2.1127],
                        "properties": {},
                    },
                    {
                        "name": "H",
                        "species": [{"element": "H", "occu": 1}],
                        "xyz": [0.6084, 2.3577, -1.5447],
                        "properties": {},
                    },
                ],
            }
        )

    def get_ase(self):
        return Atoms.fromdict(
            {
                "numbers": [
                    6,
                    6,
                    7,
                    6,
                    6,
                    6,
                    6,
                    6,
                    6,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                ],
                "positions": [
                    [2.3554, 0.8348, 0.6631],
                    [1.5219, 0.0296, -0.32],
                    [0.0, 0.0, 0.0],
                    [-0.6558, -0.8654, -1.1138],
                    [-2.1618, -1.0215, -0.9835],
                    [-0.2675, -0.5998, 1.4101],
                    [0.2466, -2.0174, 1.598],
                    [-0.5986, 1.4355, 0.0238],
                    [-0.4401, 2.2042, -1.2776],
                    [2.3048, 0.4326, 1.678],
                    [2.0679, 1.8889, 0.6861],
                    [3.4071, 0.7983, 0.3583],
                    [1.6352, 0.4327, -1.3317],
                    [1.8696, -1.0082, -0.3503],
                    [-0.4044, -0.4055, -2.0752],
                    [-0.1701, -1.8464, -1.0937],
                    [-2.4492, -1.521, -0.0549],
                    [-2.6861, -0.0647, -1.0469],
                    [-2.5322, -1.6425, -1.8067],
                    [-1.3484, -0.563, 1.5809],
                    [0.1933, 0.0706, 2.1429],
                    [0.014, -2.3532, 2.6146],
                    [1.3311, -2.0852, 1.4816],
                    [-0.2272, -2.7256, 0.9136],
                    [-1.6585, 1.3432, 0.2825],
                    [-0.1167, 1.9768, 0.8445],
                    [-0.8889, 3.1974, -1.1662],
                    [-0.9499, 1.7173, -2.1127],
                    [0.6084, 2.3577, -1.5447],
                ],
                "cell": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                "pbc": [False, False, False],
            }
        )

    def test_as_pymatgen(self):
        mol = self.conformer.as_pymatgen()
        expected = self.get_pymatgen()

        self.assertEqual(mol, expected)

    def test_from_pymatgen(self):
        new = ConformerInfo.from_pymatgen(self.get_pymatgen())

        self.assertEqual(self.conformer, new)

    def test_as_ase(self):
        conformer = self.conformer.as_ase()
        expected = self.get_ase()

        self.assertEqual(conformer, expected)

    def test_from_ase(self):
        new = ConformerInfo.from_ase(self.get_ase())

        self.assertEqual(self.conformer, new)

    def test_inequality(self):
        self.assertNotEqual(self.conformer, ["test"])

        modified = deepcopy(self.conformer)
        modified.species = ["Si", "Al"]
        self.assertNotEqual(self.conformer, modified)

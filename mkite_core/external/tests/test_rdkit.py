import unittest as ut
from pkg_resources import resource_filename

import rdkit.Chem.AllChem as Chem
from mkite_core.external.rdkit import RdkitInterface


TEST_MOL = resource_filename("mkite_core.tests.files", "tea.sdf")


class TestRdkitInterface(ut.TestCase):
    def setUp(self):
        self.mol = Chem.SDMolSupplier(TEST_MOL, removeHs=True)[0]
        self.interf = RdkitInterface(self.mol)

    def test_smiles(self):
        smiles = self.interf.smiles
        expected = "CC[N+](CC)(CC)CC"
        self.assertEqual(smiles, expected)

    def test_inchi(self):
        expected = "InChI=1S/C8H20N/c1-5-9(6-2,7-3)8-4/h5-8H2,1-4H3/q+1"
        self.assertEqual(self.interf.inchi, expected)

    def test_inchikey(self):
        expected = "CBXCPBUEXACCNR-UHFFFAOYSA-N"
        self.assertEqual(self.interf.inchikey, expected)

    def test_charge(self):
        expected = 1
        self.assertEqual(self.interf.charge, expected)

    def test_symbols(self):
        expected = ["C", "C", "N", "C", "C", "C", "C", "C", "C"]
        self.assertEqual(self.interf.symbols, expected)

    def test_formula(self):
        expected = "H20 C8 N1 +1"
        self.assertEqual(self.interf.formula, expected)

    def test_num_conf(self):
        expected = 1
        self.assertEqual(self.interf.num_conformers, expected)

from typing import List
import rdkit.Chem.AllChem as Chem

from mkite_core.models import FormulaInfo, MoleculeInfo, ConformerInfo


def get_formula_info(rdmol: Chem.Mol):
    mol = Chem.AddHs(rdmol)
    symbols = [at.GetSymbol() for at in mol.GetAtoms()]
    charge = Chem.GetFormalCharge(mol)
    return FormulaInfo.from_list(symbols, charge=charge)


def get_formula(rdmol: Chem.Mol):
    info = get_formula_info(rdmol)
    return info.name


class RdkitInterface:
    def __init__(
        self,
        mol: Chem.Mol,
        stereochemistry: bool = True,
    ):
        self.mol = mol
        self.stereochemistry = stereochemistry
        self._smiles = Chem.MolToSmiles(mol, isomericSmiles=stereochemistry)

        Chem.SanitizeMol(self.mol)

    @classmethod
    def from_smiles(cls, smiles: str) -> "RdkitInterface":
        """Creates an interface starting from a SMILES string"""
        mol = Chem.MolFromSmiles(smiles)
        return cls(mol)

    @property
    def _mol(self) -> Chem.Mol:
        return Chem.MolFromSmiles(self._smiles)

    @property
    def smiles(self) -> str:
        """Gets the canonical SMILES of a Mol. The
        double conversion is necessary to canonize
        the SMILES and eliminate hydrogens from
        the original Mol"""
        return Chem.MolToSmiles(self._mol, isomericSmiles=self.stereochemistry)

    @property
    def inchi(self) -> str:
        return Chem.MolToInchi(self._mol)

    @property
    def inchikey(self) -> str:
        return Chem.MolToInchiKey(self._mol)

    def add_hydrogens(self) -> Chem.Mol:
        return Chem.AddHs(self.mol)

    @property
    def symbols(self):
        return [at.GetSymbol() for at in self.mol.GetAtoms()]

    @property
    def charge(self):
        return Chem.GetFormalCharge(self.mol)

    @property
    def formula(self) -> str:
        return get_formula(self.mol)

    @property
    def num_conformers(self):
        return self.mol.GetNumConformers()

    def get_rdkit_conformer(self, conf_id: int):
        return self.mol.GetConformer(conf_id)

    @property
    def molecule_info(self) -> dict:
        finfo = get_formula_info(self.add_hydrogens())

        return MoleculeInfo(
            formula=finfo,
            inchikey=self.inchikey,
            smiles=self.smiles,
        )

    @property
    def conformer_info(self) -> List[dict]:
        if self.num_conformers == 0:
            return {}

        finfo = get_formula_info(self.add_hydrogens())

        results = []
        for conf in self.mol.GetConformers():
            coords = conf.GetPositions().tolist()

            conf_info = ConformerInfo(
                formula=finfo,
                species=self.symbols,
                coords=coords,
                mol=self.molecule_info,
            )

            results.append(conf_info)

        return results

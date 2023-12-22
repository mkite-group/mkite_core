import os
from typing import List
from typing import Tuple

import msgspec as msg

from .base import BaseInfo
from .formula import FormulaInfo


class MoleculeInfo(BaseInfo):
    inchikey: str
    smiles: str
    formula: FormulaInfo = None
    siteprops: dict = {}
    attributes: dict = {}

    @property
    def extra_dict_fields(self):
        return {
            "@module": "mkite.orm.mols.models",
            "@class": "Molecule",
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MoleculeInfo":
        return cls(
            inchikey=data["inchikey"],
            smiles=data["smiles"],
            siteprops=data.get("siteprops", {}),
            attributes=data.get("attributes", {}),
        )

    @classmethod
    def from_molecule(cls, molecule: "mkite.midware.models.Molecule") -> "MoleculeInfo":
        return cls(
            inchikey=molecule.inchikey,
            smiles=molecule.smiles,
            siteprops=molecule.siteprops,
            attributes=molecule.attributes,
        )

    @classmethod
    def from_rdkit(cls, mol: "rdkit.Chem.Mol", **kwargs) -> "MoleculeInfo":
        from mkite_core.external.rdkit import RdkitInterface

        minf = RdkitInterface(mol, **kwargs)

        return minf.molecule_info

    @classmethod
    def from_smiles(cls, smiles: str) -> "MoleculeInfo":
        from mkite_core.external.rdkit import RdkitInterface

        minf = RdkitInterface.from_smiles(smiles)

        return minf.molecule_info

    def as_rdkit(self) -> "rdkit.Chem.Mol":
        from mkite_core.external.rdkit import RdkitInterface

        minf = RdkitInterface.from_smiles(self.smiles)

        return minf.mol

    def __eq__(self, other: "MoleculeInfo") -> bool:
        if not isinstance(other, self.__class__):
            return False

        inchikey_eq = self.inchikey == other.inchikey
        smiles_eq = self.smiles == other.smiles
        props_eq = self.siteprops == other.siteprops
        attrs_eq = self.attributes == other.attributes

        return all([inchikey_eq, smiles_eq, props_eq, attrs_eq])


class ConformerInfo(BaseInfo):
    species: List[str]
    coords: List[Tuple[float, float, float]]
    mol: MoleculeInfo = None
    formula: FormulaInfo = None
    siteprops: dict = {}
    attributes: dict = {}

    @property
    def extra_dict_fields(self):
        return {
            "@module": "mkite.orm.mols.models",
            "@class": "Conformer",
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MoleculeInfo":
        if "mol" in data and isinstance(data["mol"], dict):
            mol = MoleculeInfo.from_dict(data["mol"])
        else:
            mol = None

        return cls(
            mol=mol,
            species=data["species"],
            coords=data["coords"],
            siteprops=data.get("siteprops", {}),
            attributes=data.get("attributes", {}),
        )

    @classmethod
    def from_conformer(
        cls, conformer: "mkite.midware.models.Conformer"
    ) -> "ConformerInfo":

        if conformer.mol is not None:
            mol = conformer.mol.as_info()
        else:
            mol = None

        return cls(
            formula=conformer.formula.as_info(),
            mol=mol,
            species=conformer.species,
            coords=conformer.coords,
            siteprops=conformer.siteprops,
            attributes=conformer.attributes,
        )

    @classmethod
    def from_rdkit(cls, mol: "rdkit.Chem.Mol", **kwargs) -> List["ConformerInfo"]:
        from mkite_core.external.rdkit import RdkitInterface

        minf = RdkitInterface(mol, **kwargs)

        return minf.conformer_info

    @classmethod
    def from_pymatgen(
        cls, molecule: "pymatgen.core.Molecule", **kwargs
    ) -> "ConformerInfo":
        return cls(
            species=[str(sp) for sp in molecule.species],
            coords=molecule.cart_coords.tolist(),
            siteprops=molecule.site_properties,
            **kwargs,
        )

    @classmethod
    def from_ase(cls, atoms: "ase.Atoms", **kwargs) -> "ConformerInfo":
        return cls(
            species=atoms.get_chemical_symbols(),
            coords=atoms.positions,
            attributes=atoms.info,
            **kwargs,
        )

    def as_pymatgen(self) -> "pymatgen.core.Molecule":
        from pymatgen.core import Molecule

        return Molecule(
            species=self.species,
            coords=self.coords,
            site_properties=self.siteprops,
        )

    def as_ase(self) -> "ase.Atoms":
        from ase import Atoms

        return Atoms(
            symbols=self.species,
            positions=self.coords,
        )

    def __eq__(self, other: "ConformerInfo") -> bool:
        import numpy as np

        if not isinstance(other, self.__class__):
            return False

        species_eq = self.species == other.species
        coords_eq = np.allclose(self.coords, other.coords)
        props_eq = self.siteprops == other.siteprops
        attrs_eq = self.attributes == other.attributes

        return all([species_eq, coords_eq, props_eq, attrs_eq])

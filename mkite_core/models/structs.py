import os
import msgspec as msg
from typing import List, Tuple

from .base import BaseInfo


class SpaceGroupInfo(BaseInfo):
    number: int
    symbol: str

    @classmethod
    def from_spacegroup(cls, spacegroup):
        return cls(number=spacegroup.value, symbol=spacegroup.label)

    @classmethod
    def from_crystal(cls, crystal: "Crystal", **kwargs):
        info = CrystalInfo.from_crystal(crystal)
        return cls.from_info(info, **kwargs)

    @classmethod
    def from_info(cls, crystal_info: "CrystalInfo", **kwargs):
        struct = crystal_info.as_pymatgen()
        symbol, number = struct.get_space_group_info(**kwargs)
        return cls(number=number, symbol=symbol)


class CrystalInfo(BaseInfo):
    species: List[str]
    coords: List[Tuple[float, float, float]]
    lattice: Tuple[
        Tuple[float, float, float],
        Tuple[float, float, float],
        Tuple[float, float, float],
    ]
    siteprops: dict = {}
    attributes: dict = {}

    @property
    def extra_dict_fields(self):
        return {
            "@module": "mkite.orm.structs.models",
            "@class": "Crystal",
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            species=data["species"],
            coords=data["coords"],
            lattice=data["lattice"],
            siteprops=data.get("siteprops", {}),
            attributes=data.get("attributes", {}),
        )

    @classmethod
    def from_crystal(cls, crystal: "mkite.orm.structs.models.Crystal") -> "CrystalInfo":
        return cls(
            species=crystal.species,
            coords=crystal.coords,
            lattice=crystal.lattice,
            siteprops=crystal.siteprops,
            attributes=crystal.attributes,
        )

    def as_pymatgen(self):
        from pymatgen.core import Structure

        return Structure(
            lattice=self.lattice,
            species=self.species,
            coords=self.coords,
            coords_are_cartesian=True,
            site_properties=self.siteprops,
        )

    def as_ase(self):
        from ase import Atoms

        return Atoms(
            cell=self.lattice,
            symbols=self.species,
            positions=self.coords,
            pbc=True,
        )

    @classmethod
    def from_pymatgen(cls, structure: "pymatgen.core.Structure", **kwargs):
        from mkite_core.external.serialization import reserialize

        return cls(
            lattice=structure.lattice.matrix.tolist(),
            species=[str(sp) for sp in structure.species],
            coords=structure.cart_coords.tolist(),
            siteprops=reserialize(structure.site_properties),
            **kwargs,
        )

    @classmethod
    def from_ase(cls, atoms: "ase.Atoms", **kwargs):
        return cls(
            lattice=atoms.cell,
            species=atoms.get_chemical_symbols(),
            coords=atoms.positions,
            attributes=atoms.info,
            **kwargs,
        )

    def __eq__(self, other: "CrystalInfo"):
        import numpy as np

        if not isinstance(other, self.__class__):
            return False

        species_eq = self.species == other.species
        coords_eq = np.allclose(self.coords, other.coords)
        lattice_eq = np.allclose(self.lattice, other.lattice)
        props_eq = self.siteprops == other.siteprops
        attrs_eq = self.attributes == other.attributes

        return all([species_eq, coords_eq, lattice_eq, props_eq, attrs_eq])

    @property
    def frac_coords(self):
        import numpy as np

        return np.array(self.coords) @ np.linalg.inv(np.array(self.lattice))

    @property
    def anonymize_species(self, start_int: int = 1):
        unique_symbols = list(set(self.symbols))
        mapper = {s: i for i, s in enumerate(unique_symbols, start_int)}
        return [mapper[sym] for sym in self.symbols]

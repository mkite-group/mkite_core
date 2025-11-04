import os
import msgspec as msg
from typing import List, Tuple, Dict

from pymatgen.core.composition import Composition
from .base import BaseInfo


class FormulaInfo(BaseInfo):
    name: str
    charge: int

    @classmethod
    def from_pymatgen(cls, composition: Composition, charge: int = None):
        def get_charge(_composition):
            charge = 0
            for e, n in _composition.items():
                if hasattr(e, "oxi_state"):
                    charge += e.oxi_state * n

            return charge

        formula = composition.formula
        charge = charge if charge is not None else get_charge(composition)
        name = f"{formula} {charge:+}"

        return cls(name, charge)

    @classmethod
    def from_list(cls, elements: List[str], charge: int = None):
        eldict = {}
        for el in elements:
            eldict[el] = eldict.get(el, 0) + 1

        return cls.from_dict(eldict, charge=charge)

    @classmethod
    def from_dict(cls, eldict: Dict[str, int], charge: int = None):
        comp = Composition(eldict)
        return cls.from_pymatgen(comp, charge=charge)

    def as_pymatgen(self):
        return Composition(self.name)

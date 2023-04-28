from typing import List

from .base import BaseInfo


class EnergyForcesInfo(BaseInfo):
    energy: float
    forces: List[List[float]] = None
    attributes: dict = {}

    @property
    def extra_dict_fields(self):
        return {
            "@module": "mkite.orm.calcs.models",
            "@class": "EnergyForces",
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            energy=data["energy"],
            forces=data["forces"],
            attributes=data["attributes"],
        )

    @classmethod
    def from_calc(
        cls, calc: "mkite.orm.calcs.models.EnergyForces"
    ) -> "EnergyForcesInfo":
        return cls(
            energy=calc.energy,
            forces=calc.forces,
            attributes=calc.attributes,
        )

    def __eq__(self, other: "EnergyForcesInfo"):
        import numpy as np

        if not isinstance(other, self.__class__):
            return False

        energy_eq = self.energy == other.energy
        forces_eq = np.allclose(self.forces, other.forces)

        return all([energy_eq, forces_eq])


class FeatureInfo(BaseInfo):
    value: List[float]
    attributes: dict = {}

    @property
    def extra_dict_fields(self):
        return {
            "@module": "mkite.orm.calcs.models",
            "@class": "Feature",
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            value=data["value"],
            attributes=data["attributes"],
        )

    @classmethod
    def from_calc(cls, calc: "mkite.orm.calcs.models.Feature") -> "FeatureInfo":
        return cls(
            value=calc.value,
            attributes=calc.attributes,
        )

    def __eq__(self, other: "FeatureInfo"):
        if not isinstance(other, self.__class__):
            return False

        return self.value == other.value

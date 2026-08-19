"""Contrato comun para verificaciones futuras."""

from dataclasses import dataclass
from enum import StrEnum


class CheckStatus(StrEnum):
    PASSES = "CUMPLE"
    FAILS = "NO CUMPLE"
    NOT_APPLICABLE = "NO APLICA"


@dataclass(frozen=True, slots=True)
class CheckResult:
    name: str
    status: CheckStatus
    demand: float | None
    capacity: float | None
    units: str
    method: str
    reference: str
    message: str

    @property
    def demand_capacity_ratio(self) -> float | None:
        if self.demand is None or self.capacity in (None, 0):
            return None
        return self.demand / self.capacity


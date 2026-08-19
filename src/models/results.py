"""Resultados estructurados del nucleo de calculo."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SectionProperties:
    area_m2: float
    centroid_from_bottom_m: float
    inertia_m4: float
    section_modulus_top_m3: float
    section_modulus_bottom_m3: float
    self_weight_n_m: float
    height_m: float


@dataclass(frozen=True, slots=True)
class ElasticStressResult:
    top_pa: float
    bottom_pa: float
    axial_component_pa: float
    prestress_moment_n_m: float
    external_moment_n_m: float
    resultant_moment_n_m: float


@dataclass(frozen=True, slots=True)
class CaseAnalysisResult:
    project_name: str
    standard: str
    section: SectionProperties
    transfer_uniform_load_n_m: float
    transfer_reaction_n: float
    transfer_max_shear_n: float
    transfer_midspan_moment_n_m: float
    transfer_stress: ElasticStressResult
    initial_steel_stress_pa: float

    def to_dict(self) -> dict[str, Any]:
        """Entrega magnitudes con unidades conservadas en los nombres."""

        return {
            "project_name": self.project_name,
            "standard": self.standard,
            "section": asdict(self.section),
            "transfer": {
                "uniform_load_n_m": self.transfer_uniform_load_n_m,
                "reaction_n": self.transfer_reaction_n,
                "max_shear_n": self.transfer_max_shear_n,
                "midspan_moment_n_m": self.transfer_midspan_moment_n_m,
                "stress": asdict(self.transfer_stress),
            },
            "prestress": {"initial_steel_stress_pa": self.initial_steel_stress_pa},
        }


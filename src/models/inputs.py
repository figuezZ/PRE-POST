"""Entradas tipadas con unidades SI explicitas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


def _require_text(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} es obligatorio")


def _require_positive(name: str, value: float) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{name} debe ser mayor que cero")


def _require_nonnegative(name: str, value: float) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} no puede ser negativo")


@dataclass(frozen=True, slots=True)
class ProjectMetadata:
    name: str
    author: str
    calculation_date: str
    version: str
    standard: str

    def __post_init__(self) -> None:
        for field_name in ("name", "author", "calculation_date", "version", "standard"):
            _require_text(field_name, getattr(self, field_name))


@dataclass(frozen=True, slots=True)
class BeamInput:
    span_m: float
    support_condition: str = "simply_supported"

    def __post_init__(self) -> None:
        _require_positive("span_m", self.span_m)
        if self.support_condition != "simply_supported":
            raise ValueError(
                "support_condition debe ser 'simply_supported' en el alcance actual"
            )


@dataclass(frozen=True, slots=True)
class RectangularSectionInput:
    width_m: float
    height_m: float

    def __post_init__(self) -> None:
        _require_positive("width_m", self.width_m)
        _require_positive("height_m", self.height_m)


@dataclass(frozen=True, slots=True)
class ConcreteInput:
    compressive_strength_transfer_pa: float
    compressive_strength_service_pa: float
    elastic_modulus_pa: float
    unit_weight_n_m3: float

    def __post_init__(self) -> None:
        for field_name in (
            "compressive_strength_transfer_pa",
            "compressive_strength_service_pa",
            "elastic_modulus_pa",
            "unit_weight_n_m3",
        ):
            _require_positive(field_name, getattr(self, field_name))
        if self.compressive_strength_service_pa < self.compressive_strength_transfer_pa:
            raise ValueError(
                "compressive_strength_service_pa no puede ser menor que la resistencia "
                "a transferencia"
            )


@dataclass(frozen=True, slots=True)
class LoadInput:
    superimposed_dead_load_n_m: float = 0.0
    live_load_n_m: float = 0.0

    def __post_init__(self) -> None:
        _require_nonnegative(
            "superimposed_dead_load_n_m", self.superimposed_dead_load_n_m
        )
        _require_nonnegative("live_load_n_m", self.live_load_n_m)


@dataclass(frozen=True, slots=True)
class PrestressInput:
    initial_force_n: float
    eccentricity_m: float
    steel_area_m2: float
    steel_ultimate_strength_pa: float

    def __post_init__(self) -> None:
        _require_positive("initial_force_n", self.initial_force_n)
        _require_positive("steel_area_m2", self.steel_area_m2)
        _require_positive("steel_ultimate_strength_pa", self.steel_ultimate_strength_pa)
        if self.initial_stress_pa > self.steel_ultimate_strength_pa:
            raise ValueError(
                "La tension inicial del acero supera su resistencia ultima declarada"
            )

    @property
    def initial_stress_pa(self) -> float:
        return self.initial_force_n / self.steel_area_m2


@dataclass(frozen=True, slots=True)
class DesignInput:
    metadata: ProjectMetadata
    beam: BeamInput
    section: RectangularSectionInput
    concrete: ConcreteInput
    loads: LoadInput
    prestress: PrestressInput

    def __post_init__(self) -> None:
        half_depth = self.section.height_m / 2.0
        if abs(self.prestress.eccentricity_m) >= half_depth:
            raise ValueError(
                "El centro del tendon debe permanecer dentro de la seccion bruta"
            )

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "DesignInput":
        """Construye y valida una entrada desde JSON u otro mapeo."""

        try:
            return cls(
                metadata=ProjectMetadata(**data["metadata"]),
                beam=BeamInput(**data["beam"]),
                section=RectangularSectionInput(**data["section"]),
                concrete=ConcreteInput(**data["concrete"]),
                loads=LoadInput(**data.get("loads", {})),
                prestress=PrestressInput(**data["prestress"]),
            )
        except KeyError as exc:
            raise ValueError(f"Falta el bloque obligatorio: {exc.args[0]}") from exc


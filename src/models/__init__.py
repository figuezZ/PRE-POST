"""Modelos de entrada y resultados estructurados."""

from .inputs import (
    BeamInput,
    ConcreteInput,
    DesignInput,
    LoadInput,
    PrestressInput,
    ProjectMetadata,
    RectangularSectionInput,
)
from .results import (
    CaseAnalysisResult,
    ElasticStressResult,
    SectionProperties,
    ServiceAnalysisResult,
)

__all__ = [
    "BeamInput",
    "CaseAnalysisResult",
    "ConcreteInput",
    "DesignInput",
    "ElasticStressResult",
    "LoadInput",
    "PrestressInput",
    "ProjectMetadata",
    "RectangularSectionInput",
    "SectionProperties",
    "ServiceAnalysisResult",
]

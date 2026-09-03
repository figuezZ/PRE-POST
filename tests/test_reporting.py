"""Pruebas de los reportes descargables de transferencia y servicio."""

from io import BytesIO

from openpyxl import load_workbook
from pypdf import PdfReader
import pytest

from src.analysis import analyze_service, analyze_transfer
from src.models import (
    BeamInput,
    ConcreteInput,
    DesignInput,
    LoadInput,
    PrestressInput,
    ProjectMetadata,
    RectangularSectionInput,
)
from src.reporting import build_excel_report, build_pdf_report, safe_report_stem


@pytest.fixture
def analyzed_design():
    design = DesignInput(
        metadata=ProjectMetadata(
            "Prueba de servicio",
            "Equipo ICIV 1042",
            "2026-08-26",
            "0.4.0",
            "ACI 318-19 (provisional)",
        ),
        beam=BeamInput(10.0),
        section=RectangularSectionInput(0.4, 0.8),
        concrete=ConcreteInput(35e6, 45e6, 34e9, 25e3),
        loads=LoadInput(2_000.0, 5_000.0),
        prestress=PrestressInput(
            initial_force_n=1_000_000.0,
            eccentricity_m=-0.20,
            steel_area_m2=0.0007,
            steel_ultimate_strength_pa=1_860e6,
            time_dependent_loss_ratio=0.15,
        ),
    )
    return design, analyze_transfer(design), analyze_service(design)


def test_excel_report_is_openable_and_contains_service_results(analyzed_design):
    design, transfer, service = analyzed_design

    report = build_excel_report(design, transfer, service)
    workbook = load_workbook(BytesIO(report), data_only=True)
    sheet = workbook["Informe PRE-POST"]
    rows = {
        sheet.cell(row=row, column=1).value: sheet.cell(row=row, column=2).value
        for row in range(1, sheet.max_row + 1)
    }

    assert report.startswith(b"PK")
    assert sheet["A1"].value == "PRE-POST | Informe de resultados"
    assert sheet.sheet_view.showGridLines is False
    assert rows["Fuerza efectiva Pe"] == pytest.approx(850.0)
    assert rows["Carga uniforme total"] == pytest.approx(15.0)
    assert rows["Tension fibra superior"] == pytest.approx(
        service.stress.top_pa / 1e6
    )


def test_pdf_report_is_openable_and_contains_traceability(analyzed_design):
    design, transfer, service = analyzed_design

    report = build_pdf_report(design, transfer, service)
    reader = PdfReader(BytesIO(report))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    assert report.startswith(b"%PDF")
    assert len(reader.pages) == 2
    assert "PRE-POST | Informe de resultados" in text
    assert "Fuerza efectiva Pe" in text
    assert "Clase 3 USS (2026)" in text
    assert "Compresion negativa" in text


def test_report_filename_is_portable():
    assert safe_report_stem("Viga Ñuble / Etapa 1", "2026-08-26") == (
        "PRE_POST_Viga_Nuble_Etapa_1_2026-08-26"
    )

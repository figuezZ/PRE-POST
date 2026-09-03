"""Interfaz Streamlit conectada al nucleo de calculo PRE-POST."""

from datetime import date
from pathlib import Path
import sys


# Streamlit Community Cloud ejecuta este archivo con `src/app` como ruta de
# importacion. Agregar la raiz permite reutilizar el paquete `src` sin duplicar
# formulas ni depender de una instalacion editable del repositorio.
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

import streamlit as st

from src import __version__
from src.analysis import (
    analyze_service,
    analyze_transfer,
    linear_fiber_stress_profile,
    uniform_load_diagram,
)
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


def _render_result_charts(design, transfer_result, service_result) -> None:
    """Presenta diagramas calculados por el nucleo, sin duplicar ecuaciones."""

    transfer_diagram = uniform_load_diagram(
        transfer_result.transfer_uniform_load_n_m,
        design.beam.span_m,
    )
    service_diagram = uniform_load_diagram(
        service_result.total_uniform_load_n_m,
        design.beam.span_m,
    )
    transfer_stress = linear_fiber_stress_profile(
        height_m=transfer_result.section.height_m,
        top_stress_pa=transfer_result.transfer_stress.top_pa,
        bottom_stress_pa=transfer_result.transfer_stress.bottom_pa,
    )
    service_stress = linear_fiber_stress_profile(
        height_m=service_result.section.height_m,
        top_stress_pa=service_result.stress.top_pa,
        bottom_stress_pa=service_result.stress.bottom_pa,
    )

    shear_rows = [
        {
            "Posicion x [m]": transfer_point.position_m,
            "Transferencia [kN]": transfer_point.shear_n / 1e3,
            "Servicio [kN]": service_point.shear_n / 1e3,
        }
        for transfer_point, service_point in zip(
            transfer_diagram, service_diagram, strict=True
        )
    ]
    moment_rows = [
        {
            "Posicion x [m]": transfer_point.position_m,
            "Transferencia [kN m]": transfer_point.moment_n_m / 1e3,
            "Servicio [kN m]": service_point.moment_n_m / 1e3,
        }
        for transfer_point, service_point in zip(
            transfer_diagram, service_diagram, strict=True
        )
    ]
    stress_rows = [
        {
            "Altura y [m]": transfer_point.elevation_from_centroid_m,
            "Transferencia [MPa]": transfer_point.stress_pa / 1e6,
            "Servicio [MPa]": service_point.stress_pa / 1e6,
        }
        for transfer_point, service_point in zip(
            transfer_stress, service_stress, strict=True
        )
    ]

    st.subheader("Graficos de resultados")
    st.caption(
        "Las curvas comparan transferencia y servicio. En tensiones, la altura "
        "positiva apunta hacia la fibra superior."
    )
    shear_tab, moment_tab, stress_tab = st.tabs(
        ("Corte V(x)", "Momento M(x)", "Tensiones en la seccion")
    )
    with shear_tab:
        st.line_chart(
            shear_rows,
            x="Posicion x [m]",
            y=("Transferencia [kN]", "Servicio [kN]"),
            color=("#2563EB", "#F59E0B"),
            width="stretch",
        )
    with moment_tab:
        st.line_chart(
            moment_rows,
            x="Posicion x [m]",
            y=("Transferencia [kN m]", "Servicio [kN m]"),
            color=("#2563EB", "#F59E0B"),
            width="stretch",
        )
    with stress_tab:
        st.line_chart(
            stress_rows,
            x="Altura y [m]",
            y=("Transferencia [MPa]", "Servicio [MPa]"),
            color=("#2563EB", "#F59E0B"),
            width="stretch",
        )
        st.caption("Convencion: compresion negativa y traccion positiva.")


def _render_transfer_service() -> None:
    with st.form("beam_input"):
        st.subheader("Entrada - transferencia y servicio")
        project_name = st.text_input("Proyecto", "Caso A - control analitico")
        author = st.text_input("Autor", "Equipo ICIV 1042")
        left, middle, right = st.columns(3)
        with left:
            span_m = st.number_input("Luz [m]", min_value=0.1, value=10.0)
            width_m = st.number_input("Ancho b [m]", min_value=0.01, value=0.40)
            height_m = st.number_input("Alto h [m]", min_value=0.01, value=0.80)
        with middle:
            unit_weight_kn_m3 = st.number_input(
                "Peso especifico [kN/m3]", min_value=0.1, value=25.0
            )
            fci_mpa = st.number_input("f'ci [MPa]", min_value=0.1, value=35.0)
            fc_mpa = st.number_input("f'c [MPa]", min_value=0.1, value=45.0)
            superimposed_dead_load_kn_m = st.number_input(
                "Carga muerta adicional [kN/m]", min_value=0.0, value=0.0
            )
            live_load_kn_m = st.number_input(
                "Carga viva de servicio [kN/m]", min_value=0.0, value=5.0
            )
        with right:
            force_kn = st.number_input(
                "Fuerza inicial Pi [kN]", min_value=0.1, value=1000.0
            )
            eccentricity_m = st.number_input(
                "Excentricidad e [m] (+ arriba)", value=-0.20
            )
            steel_area_mm2 = st.number_input(
                "Area de acero Ap [mm2]", min_value=1.0, value=700.0
            )
            time_dependent_loss_percent = st.number_input(
                "Perdida dependiente del tiempo [%]",
                min_value=0.0,
                max_value=99.9,
                value=15.0,
            )
        submitted = st.form_submit_button("Calcular etapas")

    if not submitted:
        st.info("Complete los datos y ejecute el analisis.")
        return

    try:
        design = DesignInput(
            metadata=ProjectMetadata(
                name=project_name,
                author=author,
                calculation_date=date.today().isoformat(),
                version=__version__,
                standard="ACI 318-19 (provisional)",
            ),
            beam=BeamInput(span_m=span_m),
            section=RectangularSectionInput(width_m=width_m, height_m=height_m),
            concrete=ConcreteInput(
                compressive_strength_transfer_pa=fci_mpa * 1e6,
                compressive_strength_service_pa=fc_mpa * 1e6,
                elastic_modulus_pa=34e9,
                unit_weight_n_m3=unit_weight_kn_m3 * 1e3,
            ),
            loads=LoadInput(
                superimposed_dead_load_n_m=superimposed_dead_load_kn_m * 1e3,
                live_load_n_m=live_load_kn_m * 1e3,
            ),
            prestress=PrestressInput(
                initial_force_n=force_kn * 1e3,
                eccentricity_m=eccentricity_m,
                steel_area_m2=steel_area_mm2 * 1e-6,
                steel_ultimate_strength_pa=1860e6,
                time_dependent_loss_ratio=time_dependent_loss_percent / 100.0,
            ),
        )
        transfer_result = analyze_transfer(design)
        service_result = analyze_service(design)
    except ValueError as exc:
        st.error(str(exc))
        return

    st.subheader("Resultados del nucleo")
    transfer_tab, service_tab = st.tabs(("Transferencia", "Servicio"))
    with transfer_tab:
        one, two, three = st.columns(3)
        one.metric("Area [m2]", f"{transfer_result.section.area_m2:.6f}")
        two.metric("Inercia [m4]", f"{transfer_result.section.inertia_m4:.6f}")
        three.metric(
            "Peso propio [kN/m]",
            f"{transfer_result.section.self_weight_n_m / 1e3:.3f}",
        )
        one, two, three = st.columns(3)
        one.metric(
            "Momento en centro [kN m]",
            f"{transfer_result.transfer_midspan_moment_n_m / 1e3:.3f}",
        )
        two.metric(
            "Tension fibra superior [MPa]",
            f"{transfer_result.transfer_stress.top_pa / 1e6:.3f}",
        )
        three.metric(
            "Tension fibra inferior [MPa]",
            f"{transfer_result.transfer_stress.bottom_pa / 1e6:.3f}",
        )
    with service_tab:
        st.info(
            "La perdida global es un dato del problema. Todavia no se calculan "
            "retraccion, fluencia ni relajacion por separado."
        )
        one, two, three = st.columns(3)
        one.metric(
            "Fuerza efectiva Pe [kN]",
            f"{service_result.effective_prestress_force_n / 1e3:.3f}",
        )
        two.metric(
            "Carga uniforme total [kN/m]",
            f"{service_result.total_uniform_load_n_m / 1e3:.3f}",
        )
        three.metric(
            "Momento en centro [kN m]",
            f"{service_result.midspan_moment_n_m / 1e3:.3f}",
        )
        one, two = st.columns(2)
        one.metric(
            "Tension fibra superior [MPa]",
            f"{service_result.stress.top_pa / 1e6:.3f}",
        )
        two.metric(
            "Tension fibra inferior [MPa]",
            f"{service_result.stress.bottom_pa / 1e6:.3f}",
        )
    st.caption("Convencion: compresion negativa y traccion positiva.")

    _render_result_charts(design, transfer_result, service_result)

    st.subheader("Descargar informe")
    st.caption(
        "Ambos archivos contienen los mismos datos de entrada, propiedades y "
        "resultados de transferencia y servicio."
    )
    report_stem = safe_report_stem(project_name, design.metadata.calculation_date)
    excel_report = build_excel_report(design, transfer_result, service_result)
    pdf_report = build_pdf_report(design, transfer_result, service_result)
    excel_column, pdf_column = st.columns(2)
    excel_column.download_button(
        "Descargar Excel",
        data=excel_report,
        file_name=f"{report_stem}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width="stretch",
    )
    pdf_column.download_button(
        "Descargar PDF",
        data=pdf_report,
        file_name=f"{report_stem}.pdf",
        mime="application/pdf",
        width="stretch",
    )


def main() -> None:
    st.set_page_config(page_title="PRE-POST", layout="wide")
    st.title("PRE-POST | Viga pretensada")
    st.warning(
        "Herramienta academica en desarrollo. No usar para construir obras reales."
    )
    _render_transfer_service()


if __name__ == "__main__":
    main()

"""Boceto navegable de interfaz Streamlit conectado al nucleo."""

import json
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
    simply_supported_uniform_load_at_section,
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
            force_kn = st.number_input("Fuerza inicial Pi [kN]", min_value=0.1, value=1000.0)
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
        use_container_width=True,
    )
    pdf_column.download_button(
        "Descargar PDF",
        data=pdf_report,
        file_name=f"{report_stem}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )


def _render_case_b() -> None:
    case_path = REPOSITORY_ROOT / "examples" / "case_b_ejemplo6.json"
    case = json.loads(case_path.read_text(encoding="utf-8"))
    case_input = case["input"]

    st.subheader("Caso B - Ejemplo 6 publicado")
    st.info(
        "Validacion parcial: reproduce reaccion, corte y momento en el limite "
        "de la region D. El modelo de bielas y tirantes aun no esta implementado."
    )
    st.caption(case["source"])

    geometry = case_input["section"]
    one, two, three = st.columns(3)
    one.metric("Ancho de referencia [m]", f"{geometry['width_m']:.4f}")
    two.metric("Altura de referencia [m]", f"{geometry['height_m']:.4f}")
    three.metric(
        "f'c de referencia [MPa]",
        f"{case_input['materials_for_future_checks']['concrete_strength_pa'] / 1e6:.3f}",
    )

    with st.form("case_b_input"):
        left, middle, right = st.columns(3)
        with left:
            span_m = st.number_input(
                "Luz entre apoyos [m]",
                min_value=0.1,
                value=float(case_input["span_m"]),
            )
        with middle:
            uniform_load_kn_m = st.number_input(
                "Carga ultima wu [kN/m]",
                min_value=0.0,
                value=float(case_input["factored_uniform_load_n_m"]) / 1e3,
                format="%.6f",
            )
        with right:
            position_m = st.number_input(
                "Distancia apoyo-seccion D [m]",
                min_value=0.0,
                value=float(case_input["position_from_left_support_m"]),
            )
        submitted = st.form_submit_button("Calcular solicitaciones del Caso B")

    if not submitted:
        st.info("Los valores iniciales corresponden a 30 ft, 0.30 kip/in y 75 in.")
        return

    try:
        result = simply_supported_uniform_load_at_section(
            uniform_load_n_m=uniform_load_kn_m * 1e3,
            span_m=span_m,
            position_from_left_m=position_m,
        )
    except ValueError as exc:
        st.error(str(exc))
        return

    st.subheader("Comparacion con el documento")
    expected = case["expected"]
    comparisons = [
        {
            "Resultado": "Reaccion izquierda",
            "Calculado": result.left_reaction_n / 1e3,
            "Publicado": expected["left_reaction_n"]["value"] / 1e3,
            "Unidad": "kN",
        },
        {
            "Resultado": "Corte en D",
            "Calculado": result.shear_n / 1e3,
            "Publicado": expected["shear_n"]["value"] / 1e3,
            "Unidad": "kN",
        },
        {
            "Resultado": "Momento en D",
            "Calculado": result.moment_n_m / 1e3,
            "Publicado": expected["moment_n_m"]["value"] / 1e3,
            "Unidad": "kN m",
        },
    ]
    st.table(comparisons)
    st.success("Caso B incorporado al nucleo de autovalidacion.")


def main() -> None:
    st.set_page_config(page_title="PRE-POST", layout="wide")
    st.title("PRE-POST | Viga pretensada")
    st.warning(
        "Herramienta academica en desarrollo. No usar para construir obras reales."
    )
    mode = st.radio(
        "Flujo de calculo",
        ("Caso A - transferencia y servicio", "Caso B - Ejemplo 6"),
        horizontal=True,
    )
    if mode == "Caso B - Ejemplo 6":
        _render_case_b()
    else:
        _render_transfer_service()


if __name__ == "__main__":
    main()

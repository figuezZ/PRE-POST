"""Boceto navegable de interfaz Streamlit conectado al nucleo."""

from datetime import date

import streamlit as st

from src.analysis import analyze_transfer
from src.models import (
    BeamInput,
    ConcreteInput,
    DesignInput,
    LoadInput,
    PrestressInput,
    ProjectMetadata,
    RectangularSectionInput,
)


def main() -> None:
    st.set_page_config(page_title="PRE-POST", layout="wide")
    st.title("PRE-POST | Viga pretensada")
    st.warning(
        "Herramienta academica en desarrollo. No usar para construir obras reales."
    )

    with st.form("transfer_input"):
        st.subheader("Entrada - transferencia")
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
        with right:
            force_kn = st.number_input("Fuerza inicial Pi [kN]", min_value=0.1, value=1000.0)
            eccentricity_m = st.number_input(
                "Excentricidad e [m] (+ arriba)", value=-0.20
            )
            steel_area_mm2 = st.number_input(
                "Area de acero Ap [mm2]", min_value=1.0, value=700.0
            )
        submitted = st.form_submit_button("Calcular transferencia")

    if not submitted:
        st.info("Complete los datos y ejecute el analisis.")
        return

    try:
        design = DesignInput(
            metadata=ProjectMetadata(
                name=project_name,
                author=author,
                calculation_date=date.today().isoformat(),
                version="0.1.0",
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
            loads=LoadInput(),
            prestress=PrestressInput(
                initial_force_n=force_kn * 1e3,
                eccentricity_m=eccentricity_m,
                steel_area_m2=steel_area_mm2 * 1e-6,
                steel_ultimate_strength_pa=1860e6,
            ),
        )
        result = analyze_transfer(design)
    except ValueError as exc:
        st.error(str(exc))
        return

    st.subheader("Resultados del nucleo")
    one, two, three = st.columns(3)
    one.metric("Area [m2]", f"{result.section.area_m2:.6f}")
    two.metric("Inercia [m4]", f"{result.section.inertia_m4:.6f}")
    three.metric("Peso propio [kN/m]", f"{result.section.self_weight_n_m / 1e3:.3f}")
    one, two, three = st.columns(3)
    one.metric(
        "Momento en centro [kN m]",
        f"{result.transfer_midspan_moment_n_m / 1e3:.3f}",
    )
    two.metric(
        "Tension fibra superior [MPa]",
        f"{result.transfer_stress.top_pa / 1e6:.3f}",
    )
    three.metric(
        "Tension fibra inferior [MPa]",
        f"{result.transfer_stress.bottom_pa / 1e6:.3f}",
    )
    st.caption("Convencion: compresion negativa y traccion positiva.")


if __name__ == "__main__":
    main()


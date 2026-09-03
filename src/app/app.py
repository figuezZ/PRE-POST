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
from src.units import Quantity, UnitSystem, display_unit, from_si, to_si


def _unit_label(
    label: str, quantity: Quantity, unit_system: UnitSystem
) -> str:
    """Agrega a una etiqueta la unidad visible seleccionada."""

    return f"{label} [{display_unit(unit_system, quantity).symbol}]"


def _display_value(
    value_si: float, quantity: Quantity, unit_system: UnitSystem
) -> str:
    """Formatea una magnitud SI para la interfaz sin alterar el nucleo."""

    unit = display_unit(unit_system, quantity)
    return f"{from_si(value_si, quantity, unit_system):.{unit.decimals}f}"


def _number_input_from_si(
    label: str,
    *,
    quantity: Quantity,
    unit_system: UnitSystem,
    default_si: float,
    minimum_si: float | None = None,
) -> float:
    """Solicita una magnitud en SI o USCS y devuelve su valor visible."""

    unit = display_unit(unit_system, quantity)
    kwargs = {
        "value": from_si(default_si, quantity, unit_system),
        "format": f"%.{unit.decimals}f",
        "key": f"{label}_{unit_system.value}",
    }
    if minimum_si is not None:
        kwargs["min_value"] = from_si(minimum_si, quantity, unit_system)
    return st.number_input(_unit_label(label, quantity, unit_system), **kwargs)


def _render_result_charts(
    design, transfer_result, service_result, unit_system: UnitSystem
) -> None:
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

    span_unit = display_unit(unit_system, Quantity.SPAN).symbol
    force_unit = display_unit(unit_system, Quantity.FORCE).symbol
    moment_unit = display_unit(unit_system, Quantity.MOMENT).symbol
    section_length_unit = display_unit(
        unit_system, Quantity.SECTION_LENGTH
    ).symbol
    stress_unit = display_unit(unit_system, Quantity.STRESS).symbol
    span_axis = f"Posicion x [{span_unit}]"
    transfer_force = f"Transferencia [{force_unit}]"
    service_force = f"Servicio [{force_unit}]"
    transfer_moment = f"Transferencia [{moment_unit}]"
    service_moment = f"Servicio [{moment_unit}]"
    height_axis = f"Altura y [{section_length_unit}]"
    transfer_stress_label = f"Transferencia [{stress_unit}]"
    service_stress_label = f"Servicio [{stress_unit}]"

    shear_rows = [
        {
            span_axis: from_si(
                transfer_point.position_m, Quantity.SPAN, unit_system
            ),
            transfer_force: from_si(
                transfer_point.shear_n, Quantity.FORCE, unit_system
            ),
            service_force: from_si(
                service_point.shear_n, Quantity.FORCE, unit_system
            ),
        }
        for transfer_point, service_point in zip(
            transfer_diagram, service_diagram, strict=True
        )
    ]
    moment_rows = [
        {
            span_axis: from_si(
                transfer_point.position_m, Quantity.SPAN, unit_system
            ),
            transfer_moment: from_si(
                transfer_point.moment_n_m, Quantity.MOMENT, unit_system
            ),
            service_moment: from_si(
                service_point.moment_n_m, Quantity.MOMENT, unit_system
            ),
        }
        for transfer_point, service_point in zip(
            transfer_diagram, service_diagram, strict=True
        )
    ]
    stress_rows = [
        {
            height_axis: from_si(
                transfer_point.elevation_from_centroid_m,
                Quantity.SECTION_LENGTH,
                unit_system,
            ),
            transfer_stress_label: from_si(
                transfer_point.stress_pa, Quantity.STRESS, unit_system
            ),
            service_stress_label: from_si(
                service_point.stress_pa, Quantity.STRESS, unit_system
            ),
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
            x=span_axis,
            y=(transfer_force, service_force),
            color=("#2563EB", "#F59E0B"),
            width="stretch",
        )
    with moment_tab:
        st.line_chart(
            moment_rows,
            x=span_axis,
            y=(transfer_moment, service_moment),
            color=("#2563EB", "#F59E0B"),
            width="stretch",
        )
    with stress_tab:
        st.line_chart(
            stress_rows,
            x=height_axis,
            y=(transfer_stress_label, service_stress_label),
            color=("#2563EB", "#F59E0B"),
            width="stretch",
        )
        st.caption("Convencion: compresion negativa y traccion positiva.")


def _render_transfer_service(unit_system: UnitSystem) -> None:
    with st.form("beam_input"):
        st.subheader("Entrada - transferencia y servicio")
        project_name = st.text_input("Proyecto", "Caso A - control analitico")
        author = st.text_input("Autor", "Equipo ICIV 1042")
        left, middle, right = st.columns(3)
        with left:
            span = _number_input_from_si(
                "Luz",
                quantity=Quantity.SPAN,
                unit_system=unit_system,
                default_si=10.0,
                minimum_si=0.1,
            )
            width = _number_input_from_si(
                "Ancho b",
                quantity=Quantity.SECTION_LENGTH,
                unit_system=unit_system,
                default_si=0.40,
                minimum_si=0.01,
            )
            height = _number_input_from_si(
                "Alto h",
                quantity=Quantity.SECTION_LENGTH,
                unit_system=unit_system,
                default_si=0.80,
                minimum_si=0.01,
            )
        with middle:
            unit_weight = _number_input_from_si(
                "Peso especifico",
                quantity=Quantity.UNIT_WEIGHT,
                unit_system=unit_system,
                default_si=25e3,
                minimum_si=100.0,
            )
            fci = _number_input_from_si(
                "f'ci",
                quantity=Quantity.STRESS,
                unit_system=unit_system,
                default_si=35e6,
                minimum_si=0.1e6,
            )
            fc = _number_input_from_si(
                "f'c",
                quantity=Quantity.STRESS,
                unit_system=unit_system,
                default_si=45e6,
                minimum_si=0.1e6,
            )
            superimposed_dead_load = _number_input_from_si(
                "Carga muerta adicional",
                quantity=Quantity.LINE_LOAD,
                unit_system=unit_system,
                default_si=0.0,
                minimum_si=0.0,
            )
            live_load = _number_input_from_si(
                "Carga viva de servicio",
                quantity=Quantity.LINE_LOAD,
                unit_system=unit_system,
                default_si=5e3,
                minimum_si=0.0,
            )
        with right:
            force = _number_input_from_si(
                "Fuerza inicial Pi",
                quantity=Quantity.FORCE,
                unit_system=unit_system,
                default_si=1e6,
                minimum_si=100.0,
            )
            eccentricity = _number_input_from_si(
                "Excentricidad e (+ arriba)",
                quantity=Quantity.SECTION_LENGTH,
                unit_system=unit_system,
                default_si=-0.20,
            )
            steel_area = _number_input_from_si(
                "Area de acero Ap",
                quantity=Quantity.STEEL_AREA,
                unit_system=unit_system,
                default_si=700e-6,
                minimum_si=1e-6,
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
            beam=BeamInput(
                span_m=to_si(span, Quantity.SPAN, unit_system)
            ),
            section=RectangularSectionInput(
                width_m=to_si(
                    width, Quantity.SECTION_LENGTH, unit_system
                ),
                height_m=to_si(
                    height, Quantity.SECTION_LENGTH, unit_system
                ),
            ),
            concrete=ConcreteInput(
                compressive_strength_transfer_pa=to_si(
                    fci, Quantity.STRESS, unit_system
                ),
                compressive_strength_service_pa=to_si(
                    fc, Quantity.STRESS, unit_system
                ),
                elastic_modulus_pa=34e9,
                unit_weight_n_m3=to_si(
                    unit_weight, Quantity.UNIT_WEIGHT, unit_system
                ),
            ),
            loads=LoadInput(
                superimposed_dead_load_n_m=to_si(
                    superimposed_dead_load,
                    Quantity.LINE_LOAD,
                    unit_system,
                ),
                live_load_n_m=to_si(
                    live_load, Quantity.LINE_LOAD, unit_system
                ),
            ),
            prestress=PrestressInput(
                initial_force_n=to_si(
                    force, Quantity.FORCE, unit_system
                ),
                eccentricity_m=to_si(
                    eccentricity, Quantity.SECTION_LENGTH, unit_system
                ),
                steel_area_m2=to_si(
                    steel_area, Quantity.STEEL_AREA, unit_system
                ),
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
        one.metric(
            _unit_label("Area", Quantity.SECTION_AREA, unit_system),
            _display_value(
                transfer_result.section.area_m2,
                Quantity.SECTION_AREA,
                unit_system,
            ),
        )
        two.metric(
            _unit_label("Inercia", Quantity.INERTIA, unit_system),
            _display_value(
                transfer_result.section.inertia_m4,
                Quantity.INERTIA,
                unit_system,
            ),
        )
        three.metric(
            _unit_label("Peso propio", Quantity.LINE_LOAD, unit_system),
            _display_value(
                transfer_result.section.self_weight_n_m,
                Quantity.LINE_LOAD,
                unit_system,
            ),
        )
        one, two, three = st.columns(3)
        one.metric(
            _unit_label("Momento en centro", Quantity.MOMENT, unit_system),
            _display_value(
                transfer_result.transfer_midspan_moment_n_m,
                Quantity.MOMENT,
                unit_system,
            ),
        )
        two.metric(
            _unit_label("Tension fibra superior", Quantity.STRESS, unit_system),
            _display_value(
                transfer_result.transfer_stress.top_pa,
                Quantity.STRESS,
                unit_system,
            ),
        )
        three.metric(
            _unit_label("Tension fibra inferior", Quantity.STRESS, unit_system),
            _display_value(
                transfer_result.transfer_stress.bottom_pa,
                Quantity.STRESS,
                unit_system,
            ),
        )
    with service_tab:
        st.info(
            "La perdida global es un dato del problema. Todavia no se calculan "
            "retraccion, fluencia ni relajacion por separado."
        )
        one, two, three = st.columns(3)
        one.metric(
            _unit_label("Fuerza efectiva Pe", Quantity.FORCE, unit_system),
            _display_value(
                service_result.effective_prestress_force_n,
                Quantity.FORCE,
                unit_system,
            ),
        )
        two.metric(
            _unit_label("Carga uniforme total", Quantity.LINE_LOAD, unit_system),
            _display_value(
                service_result.total_uniform_load_n_m,
                Quantity.LINE_LOAD,
                unit_system,
            ),
        )
        three.metric(
            _unit_label("Momento en centro", Quantity.MOMENT, unit_system),
            _display_value(
                service_result.midspan_moment_n_m,
                Quantity.MOMENT,
                unit_system,
            ),
        )
        one, two = st.columns(2)
        one.metric(
            _unit_label("Tension fibra superior", Quantity.STRESS, unit_system),
            _display_value(
                service_result.stress.top_pa,
                Quantity.STRESS,
                unit_system,
            ),
        )
        two.metric(
            _unit_label("Tension fibra inferior", Quantity.STRESS, unit_system),
            _display_value(
                service_result.stress.bottom_pa,
                Quantity.STRESS,
                unit_system,
            ),
        )
    st.caption("Convencion: compresion negativa y traccion positiva.")

    _render_result_charts(
        design, transfer_result, service_result, unit_system
    )

    st.subheader("Descargar informe")
    st.caption(
        "Ambos archivos contienen los mismos datos de entrada, propiedades y "
        "resultados de transferencia y servicio."
    )
    report_stem = safe_report_stem(project_name, design.metadata.calculation_date)
    excel_report = build_excel_report(
        design, transfer_result, service_result, unit_system=unit_system
    )
    pdf_report = build_pdf_report(
        design, transfer_result, service_result, unit_system=unit_system
    )
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
    unit_system = UnitSystem(
        st.radio(
            "Sistema de unidades",
            options=(UnitSystem.SI.value, UnitSystem.USCS.value),
            horizontal=True,
            help=(
                "Solo cambia las unidades de entrada, resultados, graficos e "
                "informes. El nucleo conserva los calculos en SI."
            ),
        )
    )
    st.caption(
        f"Visualizacion activa: {unit_system.value}. El nucleo calcula en SI "
        "y convierte solo en los limites de la aplicacion."
    )
    _render_transfer_service(unit_system)


if __name__ == "__main__":
    main()

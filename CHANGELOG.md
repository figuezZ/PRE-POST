# Registro de cambios

## 0.5.0 - 2026-09-03

- Agrega un selector horizontal `SI | USCS` en la parte superior de Streamlit.
- Convierte entradas USCS a las unidades SI del nucleo sin duplicar formulas.
- Presenta resultados y ejes de los graficos en el sistema seleccionado.
- Exporta Excel y PDF en SI o USCS e identifica el sistema dentro del informe.
- Incorpora conversiones exactas para pie, pulgada, libra-fuerza, kip y psi.
- Agrega pruebas de reversibilidad, integracion de interfaz y reportes USCS.

## 0.4.0 - 2026-09-03

- Retira de la interfaz, ejemplos, documentacion y autovalidacion el caso externo incorporado anteriormente.
- Conserva las funciones generales de transferencia, servicio, fuerza efectiva y exportacion.
- Agrega series numericas verificables para los diagramas de corte y momento a lo largo de la viga.
- Agrega el perfil lineal de tensiones en la altura de la seccion.
- Incorpora en Streamlit graficos comparativos de transferencia y servicio.
- Agrega pruebas unitarias de extremos, centro de luz, interpolacion y entradas invalidas.
- Reduce la autovalidacion a los casos A y S1, con once comparaciones numericas.

## 0.3.0 - 2026-08-26

- Agrega descarga de informes tabulados en Excel y PDF desde Streamlit.
- Centraliza el contenido de ambos formatos en `src/reporting/exports.py`.
- Incluye entradas, propiedades, transferencia, servicio, unidades y trazabilidad.
- Agrega pruebas que abren ambos archivos y verifican resultados representativos.

## 0.2.0 - 2026-08-25

- Agrega fuerza efectiva a partir de un porcentaje global de perdida declarado.
- Agrega la etapa elastica de servicio con peso propio, carga muerta adicional y carga viva.
- Incorpora en Streamlit resultados separados de transferencia y servicio.
- Agrega el caso docente S1 basado en la Clase 3, con cinco comparaciones numericas.
- Consolida el calculo de tension del acero para evitar formulas duplicadas.
- Documenta la diferencia entre la convencion de excentricidad de la guia y la del nucleo.
- Mantiene fuera del alcance los mecanismos separados de perdida y los limites normativos.

## 0.1.0 - 2026-08-19

- Inicializa la arquitectura modular exigida para el Avance 1.
- Agrega entradas tipadas y validaciones fisicas basicas.
- Implementa seccion rectangular, peso propio y carga uniforme.
- Implementa tensiones elasticas iniciales en transferencia.
- Agrega Caso A analitico, suite de pruebas y reporte de autovalidacion.
- Incorpora un boceto funcional de interfaz Streamlit conectado al nucleo.
- Corrige la deteccion de dependencias en Streamlit Community Cloud.
- Corrige la importacion del paquete `src` desde el punto de entrada alojado.

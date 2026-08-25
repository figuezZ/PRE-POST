# Registro de cambios

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
- Agrega el Ejemplo 6 como Caso B publicado para validar corte y momento en la region D.

# Version HTML autonoma

## Objetivo

`standalone/PRE_POST_Standalone.html` es una distribucion local de PRE-POST que
se abre directamente en un navegador. No requiere instalar Python, Streamlit,
extensiones ni dependencias, y no realiza solicitudes a internet.

## Ejecucion

1. Descargar `PRE_POST_Standalone.html`.
2. Guardarlo en cualquier carpeta del computador.
3. Abrirlo con doble clic.
4. Si Windows pregunta con que programa abrirlo, elegir Chrome, Edge o Firefox.

El archivo puede copiarse a otro computador o a un pendrive. Los datos se
procesan dentro del navegador y no se envian a un servidor.

## Funciones incluidas

- entradas en SI o USCS;
- seccion rectangular bruta;
- area, centroide, inercia y modulos resistentes;
- peso propio, reaccion, corte y momento por carga uniforme;
- transferencia con fuerza inicial;
- servicio con fuerza efectiva y perdida global declarada;
- tensiones elasticas superior e inferior;
- diagramas de corte, momento y distribucion de tensiones;
- tabla completa de entradas y resultados;
- descarga de una planilla Excel XML editable;
- impresion o guardado como PDF mediante el dialogo del navegador.

## Arquitectura

Aunque todo se entrega en un solo archivo, existen dos bloques separados:

1. `prepost-core`: conversiones, validaciones y calculos estructurales.
2. `prepost-app`: campos, pestanas, graficos, tablas y descargas.

La interfaz llama al nucleo HTML y no contiene ecuaciones estructurales. El
nucleo trabaja internamente en m, N y Pa, igual que el proyecto Python.

## Verificacion de equivalencia

`tests/test_standalone.py` ejecuta el nucleo JavaScript con Node y compara sus
resultados con `src.analysis` para el mismo caso. Se controlan area, inercia,
peso propio, fuerza efectiva, momentos y tensiones de ambas etapas. Tambien se
comprueba que el archivo no dependa de enlaces externos y que rechace un tendon
ubicado fuera de la seccion.

## Consideraciones de exportacion

El boton **Descargar Excel** genera un XML de Microsoft Excel 2003 con valores
numericos editables. Se utiliza este formato porque puede producirse sin
bibliotecas externas dentro de un unico HTML.

El boton **Imprimir / Guardar PDF** abre el dialogo de impresion del navegador.
En Chrome, Edge o Firefox se debe elegir **Guardar como PDF** como impresora o
destino. La vista de impresion contiene resultados, graficos y tablas.

Los datos ingresados no se guardan automaticamente al cerrar la pestana. Antes
de cerrar, se debe descargar Excel o guardar el PDF si se necesita conservar el
calculo.

## Alcance tecnico

La version HTML conserva el mismo alcance academico que la plataforma
Streamlit. No agrega verificaciones normativas, secciones netas o transformadas,
perdidas calculadas por mecanismo, fisuracion, flecha o resistencia.

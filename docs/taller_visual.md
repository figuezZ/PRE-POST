# Taller visual PRE-POST 0.7.0

## Objetivo y prioridades implementadas

Esta entrega desarrolla los números **1, 3 y 4 de la tabla de prioridades**:
editor visual, memoria paso a paso y visualización de tensiones. No corresponden
a la numeración de la lista de diez etapas propuesta después de esa tabla.

Se incorpora en el HTML autónomo y se ofrece dentro de Streamlit como
**Herramienta → Taller visual: secciones, memoria y tensiones**. Streamlit aloja
el mismo archivo; no mantiene una segunda copia de las ecuaciones del taller.
La calculadora rectangular anterior continúa disponible y sus entradas son
independientes. El taller conserva SI/USCS, gráficos, tablas y exportaciones.

## 1. Editor visual de secciones

### Interacción

1. Elegir SI o USCS. La geometría del taller usa metros o pulgadas; la luz,
   metros o pies. El cambio convierte los datos existentes, no los reinicia.
2. Ingresar ancho y alto de la plantilla. Estos campos no reemplazan la tabla
   hasta presionar **Aplicar plantilla**.
3. Seleccionar Rectangular, T, I asimétrica en altura o Rectangular hueca.
4. Aplicar la plantilla. Esta acción reemplaza los componentes y propone el
   tendón al 10 % de la altura desde la base; revisar su excentricidad.
5. Editar nombre, tipo, ancho b, alto h y cota inferior Y de cada componente.
6. Agregar sólidos o vacíos, o quitar componentes. Las dimensiones no se
   ajustan automáticamente entre filas: sus caras deben coincidir.
7. Revisar el dibujo, el mensaje geométrico y la posición del tendón.
8. Presionar **Calcular etapas**.

El dibujo se actualiza al editar, conserva la escala geométrica y muestra ancho,
altura, centroide, eje vertical, tendón equivalente y excentricidad.

### Representación y restricciones

Cada componente es `{name, sign, b, h, y}` en unidades internas SI:

| Campo | Significado |
|---|---|
| name | Identificador libre |
| sign | +1 para sólido; −1 para vacío |
| b, h | Ancho y altura positivos |
| y | Cota inferior desde la base, no distancia al centroide |

Todos los rectángulos se centran horizontalmente en el mismo eje. Los sólidos
deben estar apilados, tocarse por sus caras y comenzar en Y = 0. Se rechazan
superposiciones, separaciones, vacíos superpuestos, vacíos más anchos que su
sólido y geometrías completamente separadas por vacíos.

Cada vacío debe caber en un solo sólido. Puede tocar el borde superior o inferior
para representar un rebaje centrado; no puede atravesar y dividir toda la
sección en dos piezas. Los huecos rectangulares no representan automáticamente
ductos circulares: esa geometría se añadirá con sus propias integrales y pruebas.

Se admiten hasta 24 componentes. No hay edición libre por arrastre ni polígonos
arbitrarios. El tendón se representa mediante **una resultante equivalente** en
el eje vertical. La interfaz comprueba que esté en el hormigón, no en un vacío;
no comprueba recubrimiento, separación entre torones ni requisitos de anclaje.

### Propiedades calculadas

Para cada componente, con s igual a +1 o −1:

```text
Aᵢ = sᵢ bᵢ hᵢ
Yᵢ = Yinferior,ᵢ + hᵢ/2
A = Σ Aᵢ
Ȳ = Σ(Aᵢ Yᵢ)/A
dᵢ = Yᵢ − Ȳ
I = Σ(sᵢ bᵢ hᵢ³/12 + Aᵢ dᵢ²)
c_superior = h − Ȳ
c_inferior = Ȳ
W_superior = I/c_superior
W_inferior = I/c_inferior
wpp = γ A
```

La tabla distingue las propiedades brutas (sumando sólidos, antes de descontar
los vacíos declarados) y las propiedades de hormigón utilizadas para el cálculo.
El peso propio usa el área descontando vacíos. La cantidad de acero no se resta
del área ni aporta rigidez: la sección transformada sigue pendiente. La palabra
"neta" aquí solo describe el descuento geométrico de los vacíos introducidos,
no una definición normativa completa de sección neta.

### Control manual independiente de una T

Usar ancho exterior 0.40 m y alto 0.80 m:

| Componente | b [m] | h [m] | Y inferior [m] |
|---|---:|---:|---:|
| Alma | 0.12 | 0.64 | 0 |
| Ala superior | 0.40 | 0.16 | 0.64 |

Valores de control:

- A = 0.1408 m².
- Ȳ = 0.5018181818 m desde la base.
- I = 0.008343427879 m⁴.
- c_superior = 0.2981818182 m.
- c_inferior = 0.5018181818 m.
- Para γ = 25000 N/m³: wpp = 3520 N/m.

La diferencia entre las dos distancias a las fibras explica por qué no es
correcto conservar h/2 cuando se pasa del rectángulo a una T.

## 3. Memoria de cálculo paso a paso

La memoria contiene 19 desarrollos para la etapa y posición seleccionadas:
área, centroide, inercia, ambas distancias a fibras, ambos módulos resistentes,
peso propio, fuerza, tensión de acero, carga, reacción, corte, momento externo,
momento del pretensado, momento resultante, esfuerzo axial uniforme y tensiones
superior/inferior.

Cada bloque desplegable contiene:

- nombre y resultado con unidad;
- expresión simbólica;
- sustitución numérica;
- resultado numérico reproducible;
- referencia y convención aplicables.

La tabla previa desglosa Aᵢ, Yᵢ, dᵢ, Iᵢ, Aᵢdᵢ² y aporte total. Los vacíos aparecen
con signo negativo, permitiendo reconstruir la suma. Para evitar mezclas de
unidades, las sustituciones usan **m, N y Pa incluso en modo USCS**; los demás
resultados y gráficos siguen el sistema elegido. La notación científica de la
memoria preserva cifras significativas.

La impresión abre todos los desarrollos temporalmente y restaura los bloques
al terminar. El Excel XML incluye la memoria seleccionada y los componentes,
además del informe existente. Es una instantánea numérica, no una planilla que
recalcula las fórmulas al editarla. La sección transformada y verificaciones ACI
no se simulan ni se presentan como cumplidas.

## 4. Explorador de tensiones

### Controles

- Etapa: transferencia o servicio.
- Posición x/L: desde el apoyo izquierdo al derecho, en incrementos de 0.005 L.
- Fibra Y/h: desde la base a la parte superior, en incrementos de 0.005 h.

El mapa, las magnitudes de la fibra y la memoria cambian conjuntamente. Los
indicadores originales y el perfil comparativo existente siguen mostrando
**centro de luz**, mientras que el explorador indica explícitamente su x.

### Modelo mecánico

Con P = Pi en transferencia y P = (1 − pérdida) Pi en servicio:

```text
R = wL/2
V(x) = R − wx
M(x) = Rx − wx²/2
Mp = P e
Mr = Mp + M(x)
σ(y,x) = −P/A − Mr y/I
```

La fibra se muestra en coordenada y relativa al centroide, con tres aportes:
axial −P/A, pretensado −Pey/I y flexión externa −My/I. Su suma reproduce la
tensión total. Compresión es negativa; tracción, positiva.

El color azul identifica compresión, rojo tracción y blanco el entorno de cero.
Los vacíos se dibujan blancos con borde discontinuo: no están coloreados como
hormigón. Si el punto central de la fibra seleccionada cae en un vacío o borde,
se advierte que el valor corresponde a la prolongación del campo elástico.

La escala es simétrica y fija para el cálculo: usa la máxima tensión absoluta
de ambas etapas entre apoyos y centro de luz. Para carga uniforme y sección
constante esos puntos abarcan los extremos del campo lineal analizado. Cambiar
de etapa no altera artificialmente la escala. El color no indica "cumple".

La línea σ = 0 se muestra únicamente si su posición cae dentro de la altura:

```text
k = −Mr/I
y_cero = −σ_axial/k  (si k ≠ 0)
```

El centroide geométrico y la línea de tensión nula no son lo mismo. Si hay
compresión uniforme o la raíz está fuera de la altura, se explica que no hay
línea de tensión nula dentro de la sección.

## Integración y archivos

| Pieza | Responsabilidad |
|---|---|
| HTML, bloque prepost-core | Geometría, propiedades, equilibrio, tensiones y memoria numérica |
| HTML, bloque prepost-app | Editor, dibujo SVG, controles, impresión y Excel XML |
| src/app/app.py | Selector de herramienta, alojamiento del HTML y descarga local |
| tests/test_visual_workshop.py | Integrales independientes, controles geométricos, equilibrio y memoria |
| tests/test_standalone.py | Equivalencia con el flujo rectangular Python y archivo autónomo |

Modificar datos invalida los resultados para evitar exportar un cálculo viejo.
No hay guardado automático entre sesiones. Descargar el HTML conserva la
aplicación; descargar Excel o imprimir conserva los resultados actuales.

## Referencias y evidencia

- Geometría: definiciones integrales A = ∫dA, Q = ∫Y dA y I = ∫(Y−Ȳ)² dA;
  desarrollo mediante el teorema de ejes paralelos.
- Estática: equilibrio de viga simplemente apoyada bajo carga uniforme.
- Tensiones y fuerzas por etapas: Clase 3 USS (2026), ecuaciones (25)–(28),
  material docente ya incorporado; ver docs/caso_servicio_clase3.md.
- Convenciones heredadas: docs/caso_a_analitico.md y AGENTS.md.

Las pruebas de geometría integran respecto de la base y trasladan el segundo
momento al centroide: no copian la suma componente por componente del código JS.
Comprueban también ∫σ dA = −P y ∫σy dA = −Mr, los apoyos y centro de luz,
campos de compresión uniforme y la coherencia de los 19 desarrollos.

No se hizo una verificación visual en todos los navegadores. La verificación
automática cubre sintaxis JS, núcleo numérico y alojamiento en Streamlit, no
certifica el comportamiento de impresión de cada navegador.

## Guion sugerido de demostración al profesor

1. Abrir el HTML local sin conexión y resolver el rectángulo de control.
2. Aplicar la T y explicar el desplazamiento del centroide.
3. Abrir la tabla de aportes y reconstruir el área y la inercia.
4. Elegir Servicio y desplazar x/L desde 0 hasta 0.5.
5. Observar el mapa, la línea σ = 0 cuando exista y los tres aportes de tensión.
6. Abrir el desarrollo de tensión superior y relacionarlo con el dibujo.
7. Cambiar a USCS: las unidades cambian, la geometría física no.
8. Descargar Excel e imprimir la memoria local como PDF.
9. Explicar qué permanece pendiente: sección transformada, pérdidas por
   mecanismos, fisuración, flecha, resistencia y comprobaciones normativas.

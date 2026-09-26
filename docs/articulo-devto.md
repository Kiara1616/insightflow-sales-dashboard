---
title: "Del dato al indicador: diseño de un dashboard de ventas reproducible con Streamlit"
description: "Un caso práctico de modelado de indicadores, visualización interactiva, pruebas automatizadas y publicación continua en la nube."
tags: python, streamlit, dataviz, github
---

Un dashboard es útil cuando responde preguntas concretas y permite verificar de dónde salen sus cifras. En este trabajo construí un panel de análisis comercial que transforma un archivo de transacciones en indicadores, comparaciones y vistas filtrables. El resultado está disponible públicamente y su código puede reproducirse.

> **Explora el proyecto:** [aplicación interactiva](https://insightflow-sales-dashboard-he3kljwft48fj5lkjgtyu.streamlit.app) · [repositorio público y código fuente](https://github.com/Kiara1616/insightflow-sales-dashboard) · [pruebas automatizadas](https://github.com/Kiara1616/insightflow-sales-dashboard/actions)

Los datos utilizados son **demostrativos**. El objetivo es evaluar una forma de organizar el análisis y la publicación de un dashboard, no describir el desempeño de una empresa real.

## 1. Pregunta de análisis y alcance

El punto de partida fue una necesidad frecuente: una tabla de operaciones permite buscar registros individuales, pero dificulta comparar períodos, regiones y líneas de producto de manera inmediata. El panel se diseñó para responder cuatro preguntas:

1. ¿Cuál es el volumen de ventas y de unidades en el período seleccionado?
2. ¿Cómo cambian las ventas de un mes a otro?
3. ¿Qué regiones y categorías concentran la facturación?
4. ¿Qué producto registra la mayor venta acumulada bajo los filtros actuales?

La solución es descriptiva. No predice demanda ni establece causas de las diferencias observadas. Para ello se necesitarían más datos y otro diseño analítico.

## 2. Datos y definición de indicadores

El archivo [`data/ventas.csv`](https://github.com/Kiara1616/insightflow-sales-dashboard/blob/main/data/ventas.csv) contiene 18 registros de ejemplo fechados entre enero y junio de 2025. Cada fila incluye `fecha`, `region`, `categoria`, `producto`, `ventas` y `unidades`. Se utiliza el sol peruano (`S/`) como unidad monetaria de presentación.

Antes de visualizar, la aplicación convierte `fecha` a tipo fecha, comprueba que estén presentes las columnas requeridas y deriva un campo `mes`. Estas operaciones están implementadas en [`app.py`](https://github.com/Kiara1616/insightflow-sales-dashboard/blob/main/app.py). La validación de presencia de columnas evita que un archivo con un esquema incompatible se represente como si fuera correcto.

Los indicadores se calculan **después** de aplicar los filtros de región, categoría y período:

| Indicador | Definición |
| --- | --- |
| Ventas totales | Suma de `ventas` en los registros filtrados. |
| Unidades vendidas | Suma de `unidades` en los registros filtrados. |
| Venta promedio por unidad | Ventas totales divididas entre unidades vendidas. |
| Producto líder | Producto con mayor suma de `ventas` dentro del subconjunto filtrado. |

La venta promedio por unidad **no es el ticket promedio por transacción**: el conjunto de datos no incluye un identificador de pedido. Precisar esta diferencia evita interpretar un indicador con una unidad de análisis equivocada. Si los filtros no devuelven registros, el panel comunica que no hay datos y no muestra métricas vacías como si fueran resultados.

## 3. Diseño del dashboard

La interfaz se construyó con [Streamlit](https://docs.streamlit.io/) y el tratamiento de datos con Pandas. Los filtros están en una barra lateral y las métricas principales se sitúan antes de los gráficos. Esta disposición permite primero leer el panorama general y luego examinar sus componentes.

La evolución temporal se representa con una línea de ventas mensuales; la comparación territorial, con barras por región. Ambas figuras se generan con [Plotly Express](https://plotly.com/python/plotly-express/). La tabla por categoría y la vista desplegable de registros conservan el detalle necesario para revisar las agregaciones.

Una decisión de implementación importante fue calcular todas las vistas a partir del mismo subconjunto filtrado. Por ejemplo:

```python
filtered = data[
    data["region"].isin(regions)
    & data["categoria"].isin(categories)
    & data["fecha"].dt.date.between(start_date, end_date)
].copy()

total_sales = filtered["ventas"].sum()
total_units = filtered["unidades"].sum()
```

Así, el valor de las tarjetas, las series y las tablas responde a la misma selección del usuario. El diseño también se revisó en temas claro y oscuro para conservar el contraste de las cifras.

## 4. Reproducibilidad y automatización

El [repositorio de InsightFlow Sales Dashboard](https://github.com/Kiara1616/insightflow-sales-dashboard) reúne el código de la aplicación, los datos de ejemplo, las dependencias, las pruebas y la configuración de integración continua. Se puede ejecutar localmente con:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Las pruebas comprueban que el archivo de datos exista, que tenga las columnas previstas, que la fecha se procese correctamente y que ventas y unidades sean positivas. El [workflow de GitHub Actions](https://github.com/Kiara1616/insightflow-sales-dashboard/blob/main/.github/workflows/tests.yml) instala las dependencias y ejecuta `python -m pytest -q` en cada `push` y `pull request`. Puede consultarse [una ejecución satisfactoria](https://github.com/Kiara1616/insightflow-sales-dashboard/actions/runs/36220497285).

El despliegue sigue otro mecanismo: [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud) toma el proyecto desde la rama `main` y publica la aplicación. La plataforma detecta cambios en el repositorio y actualiza la aplicación. Por tanto, GitHub Actions automatiza la **verificación**, mientras Streamlit Community Cloud automatiza la **actualización del despliegue**. Son procesos relacionados, pero cumplen funciones diferentes.

## 5. Resultado y límites

El resultado es un [dashboard público](https://insightflow-sales-dashboard-he3kljwft48fj5lkjgtyu.streamlit.app) que permite explorar los mismos datos desde distintas selecciones sin modificar el código. El repositorio abierto facilita revisar los cálculos y repetir la ejecución. La automatización reduce el riesgo de publicar cambios que rompan las comprobaciones básicas de los datos.

El caso tiene límites claros. El conjunto de datos es pequeño y sintético; no hay información sobre costos, márgenes, clientes ni pedidos. Por ello, el panel sirve como demostración metodológica y no como diagnóstico de un negocio. Además, las pruebas actuales validan el esquema y valores básicos, pero no cubren todas las interacciones de la interfaz ni sustituyen una revisión visual posterior al despliegue.

## Conclusión

Construir un dashboard requiere algo más que elegir gráficos. La utilidad del resultado depende de definir bien los indicadores, mantener coherencia entre filtros y visualizaciones, documentar el origen de los datos y asegurar que el proceso de publicación sea repetible. Este proyecto presenta una implementación pequeña y verificable de ese flujo. Un paso siguiente sería incorporar un conjunto de datos real, ampliar las pruebas y evaluar el panel con usuarios que tomen decisiones a partir de sus resultados.

**Recursos del proyecto:** [código y documentación](https://github.com/Kiara1616/insightflow-sales-dashboard) · [aplicación en la nube](https://insightflow-sales-dashboard-he3kljwft48fj5lkjgtyu.streamlit.app) · [historial de automatización](https://github.com/Kiara1616/insightflow-sales-dashboard/actions).

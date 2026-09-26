# InsightFlow Sales Dashboard

Panel interactivo para explorar el rendimiento de ventas por período, región, categoría y producto.

**[Explorar el dashboard](https://insightflow-sales-dashboard-he3kljwft48fj5lkjgtyu.streamlit.app)** · **[Leer el estudio técnico](docs/articulo-devto.md)** · **[Ver la automatización](https://github.com/Kiara1616/insightflow-sales-dashboard/actions)**

## Qué permite analizar

- Ventas totales, unidades vendidas, venta promedio por unidad y producto con mayor facturación.
- Evolución mensual de las ventas y comparación entre regiones.
- Resumen por categoría y consulta de los registros filtrados.
- Selección interactiva de regiones, categorías y fechas.

Los datos de `data/ventas.csv` son **datos de ejemplo** incluidos para demostrar el funcionamiento del panel. No representan ventas reales ni deben utilizarse para tomar decisiones comerciales.

## Tecnologías y estructura

La aplicación utiliza **Streamlit** para la interfaz, **Pandas** para preparar y agrupar los datos, y **Plotly** para los gráficos. Las comprobaciones se ejecutan con **Pytest** y se automatizan mediante **GitHub Actions** en cada `push` y `pull request`.

```text
app.py                       Aplicación y lógica de visualización
data/ventas.csv              Datos de demostración
tests/test_app.py             Validaciones del conjunto de datos
.github/workflows/tests.yml  Integración continua
requirements.txt             Dependencias de Python
```

## Ejecutar en local

Requiere Python 3.12. Desde la raíz del repositorio:

```bash
python -m venv .venv
```

En Windows PowerShell, activa el entorno con `.venv\Scripts\Activate.ps1`; en macOS o Linux, usa `source .venv/bin/activate`. Después ejecuta:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`.

## Calidad del proyecto

Ejecuta las pruebas localmente con `python -m pytest -q`. El [flujo de integración continua](.github/workflows/tests.yml) repite estas comprobaciones automáticamente en GitHub. La versión pública se actualiza desde la rama `main` en Streamlit Community Cloud.

## Estudio técnico

El [artículo del proyecto](docs/articulo-devto.md) documenta la pregunta de análisis, las definiciones de los indicadores, las decisiones de visualización, la automatización y las limitaciones de los datos.

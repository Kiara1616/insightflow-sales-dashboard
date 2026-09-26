# 📊 InsightFlow Sales Dashboard

Proyecto de la **Actividad Grupal 01: Visualization Reports or Dashboard** para el equipo de `Kiara1616`.

**InsightFlow** es un panel comercial interactivo para convertir registros de ventas en información útil para la toma de decisiones. El nombre se utilizará como identidad del proyecto en el repositorio, la aplicación publicada y el artículo técnico.

El dashboard permite analizar ventas por periodo, región, categoría y producto. Incluye indicadores principales, gráficos interactivos y una tabla de detalle.

## Ejecutar localmente

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`.

## Pruebas automatizadas

```bash
pytest -q
```

Cada `push` y cada `pull request` ejecuta automáticamente las pruebas mediante [GitHub Actions](.github/workflows/tests.yml).

## Despliegue en Streamlit Community Cloud

1. Crear un repositorio público en GitHub y subir todos los archivos.
2. Entrar en [share.streamlit.io](https://share.streamlit.io/) con la cuenta de GitHub.
3. Seleccionar **Create app**.
4. Elegir el repositorio, la rama `main` y el archivo `app.py`.
5. Pulsar **Deploy**.

La aplicación no requiere secretos: los datos de demostración están en `data/ventas.csv`.

## Tecnologías

- Python 3.12
- Streamlit
- Pandas
- Plotly
- Pytest
- GitHub Actions
- Streamlit Community Cloud

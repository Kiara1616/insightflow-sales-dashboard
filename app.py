from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).parent / "data" / "ventas.csv"
REQUIRED_COLUMNS = {
    "fecha",
    "region",
    "categoria",
    "producto",
    "ventas",
    "unidades",
}


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Carga y normaliza el conjunto de datos del dashboard."""
    data = pd.read_csv(path, parse_dates=["fecha"])
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(sorted(missing))}")
    data["mes"] = data["fecha"].dt.to_period("M").astype(str)
    return data


def build_dashboard(data: pd.DataFrame) -> None:
    """Renderiza el dashboard a partir de un DataFrame ya filtrado."""
    import plotly.express as px
    import streamlit as st

    st.title("Panel de análisis comercial")
    st.caption("Resumen interactivo del rendimiento comercial")

    with st.sidebar:
        st.header("Filtros")
        regions = st.multiselect("Región", sorted(data["region"].unique()), default=sorted(data["region"].unique()))
        categories = st.multiselect(
            "Categoría",
            sorted(data["categoria"].unique()),
            default=sorted(data["categoria"].unique()),
        )
        min_date = data["fecha"].min().date()
        max_date = data["fecha"].max().date()
        date_range = st.date_input("Periodo", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    if len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date, end_date = date_range

    filtered = data[
        data["region"].isin(regions)
        & data["categoria"].isin(categories)
        & data["fecha"].dt.date.between(start_date, end_date)
    ].copy()

    if filtered.empty:
        st.warning("No hay registros para los filtros seleccionados.")
        return

    total_sales = filtered["ventas"].sum()
    total_units = filtered["unidades"].sum()
    avg_ticket = total_sales / total_units if total_units else 0
    top_product = filtered.groupby("producto")["ventas"].sum().idxmax()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ventas totales", f"S/ {total_sales:,.0f}")
    col2.metric("Unidades vendidas", f"{total_units:,.0f}")
    col3.metric("Venta promedio/unidad", f"S/ {avg_ticket:,.2f}")
    col4.metric("Producto líder", top_product)

    left, right = st.columns(2)
    with left:
        monthly = filtered.groupby("mes", as_index=False)["ventas"].sum()
        fig_monthly = px.line(monthly, x="mes", y="ventas", markers=True, title="Ventas mensuales")
        fig_monthly.update_layout(yaxis_title="Ventas (S/)", xaxis_title="Mes")
        st.plotly_chart(fig_monthly, use_container_width=True)

    with right:
        by_region = filtered.groupby("region", as_index=False)["ventas"].sum().sort_values("ventas", ascending=False)
        fig_region = px.bar(by_region, x="region", y="ventas", color="region", title="Ventas por región")
        fig_region.update_layout(showlegend=False, yaxis_title="Ventas (S/)", xaxis_title="Región")
        st.plotly_chart(fig_region, use_container_width=True)

    by_category = filtered.groupby("categoria", as_index=False).agg(ventas=("ventas", "sum"), unidades=("unidades", "sum"))
    st.subheader("Resumen por categoría")
    st.dataframe(by_category.sort_values("ventas", ascending=False), use_container_width=True, hide_index=True)

    with st.expander("Ver datos filtrados"):
        st.dataframe(filtered.sort_values("fecha", ascending=False), use_container_width=True, hide_index=True)


def main() -> None:
    import streamlit as st

    st.set_page_config(
        page_title="Panel de análisis comercial",
        page_icon=None,
        layout="wide",
    )
    st.markdown(
        """
        <style>
        .block-container { padding-top: 2.2rem; padding-bottom: 2rem; }
        [data-testid="stMetric"] {
            background: var(--secondary-background-color);
            color: var(--text-color);
            border: 1px solid color-mix(in srgb, var(--text-color) 15%, transparent);
            padding: 1rem;
            border-radius: 0.6rem;
        }
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
            color: var(--text-color);
        }
        h1 { letter-spacing: -0.02em; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    data = load_data()
    build_dashboard(data)


if __name__ == "__main__":
    main()

import plotly.express as px
import streamlit as st

import calculations

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


def trend_line_chart(monthly_df):
    fig = px.line(
        monthly_df,
        x="date",
        y="total_amount",
        markers=True,
        labels={"date": "Month", "total_amount": "Sales ($)"},
        title="Sales Trend Over Time",
    )
    fig.update_xaxes(dtick="M1", tickformat="%b %Y")
    return fig


def category_bar_chart(category_df):
    return px.bar(
        category_df,
        x="category",
        y="total_amount",
        labels={"category": "Category", "total_amount": "Sales ($)"},
        title="Sales by Category",
    )


def region_bar_chart(region_df):
    return px.bar(
        region_df,
        x="region",
        y="total_amount",
        labels={"region": "Region", "total_amount": "Sales ($)"},
        title="Sales by Region",
    )


try:
    df = calculations.load_data("data/sales-data.csv")
except Exception as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()

st.title("ShopSmart Sales Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${calculations.total_sales(df):,.0f}")
col2.metric("Total Orders", f"{calculations.total_orders(df):,}")

st.plotly_chart(trend_line_chart(calculations.monthly_trend(df)), use_container_width=True)

col3, col4 = st.columns(2)
col3.plotly_chart(category_bar_chart(calculations.sales_by_category(df)), use_container_width=True)
col4.plotly_chart(region_bar_chart(calculations.sales_by_region(df)), use_container_width=True)

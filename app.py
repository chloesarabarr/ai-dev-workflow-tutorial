import streamlit as st

import calculations

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

try:
    df = calculations.load_data("data/sales-data.csv")
except Exception as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()

st.title("ShopSmart Sales Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${calculations.total_sales(df):,.0f}")
col2.metric("Total Orders", f"{calculations.total_orders(df):,}")

import streamlit as st

import calculations

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

try:
    df = calculations.load_data("data/sales-data.csv")
except Exception as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()

st.title("ShopSmart Sales Dashboard")

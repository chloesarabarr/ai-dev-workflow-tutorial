import pandas as pd


def load_data(path):
    return pd.read_csv(path, parse_dates=["date"])


def total_sales(df):
    return df["total_amount"].sum()


def total_orders(df):
    return df["order_id"].nunique()

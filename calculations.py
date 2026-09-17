import pandas as pd


def load_data(path):
    return pd.read_csv(path, parse_dates=["date"])


def total_sales(df):
    return df["total_amount"].sum()


def total_orders(df):
    return df["order_id"].nunique()


def monthly_trend(df):
    monthly = (
        df.groupby(df["date"].dt.to_period("M"))["total_amount"]
        .sum()
        .reset_index()
    )
    monthly["date"] = monthly["date"].dt.to_timestamp()
    return monthly.sort_values("date").reset_index(drop=True)


def sales_by_category(df):
    result = df.groupby("category")["total_amount"].sum().reset_index()
    return result.sort_values("total_amount", ascending=False).reset_index(drop=True)


def sales_by_region(df):
    result = df.groupby("region")["total_amount"].sum().reset_index()
    return result.sort_values("total_amount", ascending=False).reset_index(drop=True)

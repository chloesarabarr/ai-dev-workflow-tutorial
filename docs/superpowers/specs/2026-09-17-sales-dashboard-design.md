# Design: E-Commerce Sales Dashboard

Source requirements: [`prd/ecommerce-analytics.md`](../../../prd/ecommerce-analytics.md) (Phase 1 only). Milestones tracked in [`TASKS.md`](../../../TASKS.md) (TASK-1 through TASK-7).

## Summary

A single-page Streamlit dashboard reading `data/sales-data.csv` and showing two KPI cards (Total Sales, Total Orders), a monthly sales trend line chart, and category/region bar charts, built with Pandas for data work and Plotly for interactive charts. Matches the PRD's own layout mockup and its definition of "Dashboard" as everything visible on one screen — no tabs, no sidebar navigation, no filtering (explicitly Phase 2 / out of scope).

## Architecture & file structure

```
app.py                  # Streamlit UI: page config, layout, calls into calculations.py
calculations.py         # Pure functions: load_data(), total_sales(), total_orders(),
                         #   monthly_trend(), sales_by_category(), sales_by_region()
tests/
  test_calculations.py  # pytest tests for the functions above (TDD)
data/sales-data.csv     # already exists (PRD Data Specification)
requirements.txt        # streamlit, pandas, plotly, pytest
venv/                   # local virtual environment (gitignored)
```

`app.py` never computes aggregates directly — it calls `calculations.py` functions and passes the results to `st.metric()` and Plotly chart builders. This keeps the tested logic (`calculations.py`) independent of Streamlit, and keeps `app.py` focused on layout and rendering.

## Data layer (`calculations.py`)

All functions take/return plain pandas objects, with no currency or number formatting (formatting is a display concern, handled in `app.py`).

| Function | Behavior |
|---|---|
| `load_data(path)` | Reads the CSV with `pd.read_csv(path, parse_dates=["date"])`. Raises a clear exception if the file is missing or fails to parse — `app.py` catches this and shows a friendly in-app error (see below), never a raw traceback. |
| `total_sales(df)` | Sum of `total_amount` across all rows. |
| `total_orders(df)` | Count of unique `order_id` values (482 in the sample dataset). |
| `monthly_trend(df)` | Groups by calendar month, sums `total_amount`, sorted chronologically. Monthly granularity was chosen over daily: 482 records over 12 months (~40/month) makes a daily line noisy, and the PRD's own mockup labels months (Jan, Feb, Mar, ...). |
| `sales_by_category(df)` | Groups by `category`, sums `total_amount`, sorted descending by value (FR-3). |
| `sales_by_region(df)` | Groups by `region`, sums `total_amount`, sorted descending by value (FR-4). |

## UI layer (`app.py`) & error handling

```python
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

st.plotly_chart(trend_line_chart(calculations.monthly_trend(df)))

col3, col4 = st.columns(2)
col3.plotly_chart(category_bar_chart(calculations.sales_by_category(df)))
col4.plotly_chart(region_bar_chart(calculations.sales_by_region(df)))
```

Layout mirrors the PRD's mockup: KPI row → trend chart (full width) → category/region charts side by side. Plotly charts carry interactive hover tooltips by default, satisfying the tooltip requirement in FR-2/FR-3/FR-4 with no extra code.

**Page title:** "ShopSmart Sales Dashboard" — the PRD's Executive Summary and user stories consistently use "ShopSmart"; the ASCII mockup's "SHOPMART" header is treated as a typo in the source document.

**Missing/malformed data file:** `load_data` raises, `app.py` catches it and shows `st.error(...)` followed by `st.stop()`, so the user sees a readable message instead of a Python traceback. Satisfies NFR-2 ("no training required") and the acceptance criterion "No errors: Dashboard runs without errors or warnings" by failing gracefully rather than crashing loudly.

Chart-building helpers (`trend_line_chart`, `category_bar_chart`, `region_bar_chart`) live in `app.py` since they render Plotly figures — not unit-tested, per the general difficulty of meaningfully testing UI components in isolation.

## Testing strategy

- `tests/test_calculations.py` covers every function in `calculations.py`, written test-first (TDD) against `data/sales-data.csv`. Includes assertions tying directly back to the PRD's Expected Output table: `total_sales` ≈ $116,500, `total_orders` == 482.
- `app.py`'s rendering code is verified manually: run `streamlit run app.py` locally and check the running dashboard against the PRD's Acceptance Criteria section, per the Definition of Done in `TASKS.md`.

## Out of scope (Phase 2, per PRD)

No code, stubs, or placeholder UI for: user authentication, real-time database integration, export (PDF/Excel), email alerts, filtering/date-range selection, drill-down to transaction detail, or mobile-responsive design.

## Deployment

Deployment to Streamlit Community Cloud (TASK-7 / PRD milestone M7) is planned as the implementation plan's final step, but executed by the user (not Claude) from `main` after the branch is reviewed and merged.

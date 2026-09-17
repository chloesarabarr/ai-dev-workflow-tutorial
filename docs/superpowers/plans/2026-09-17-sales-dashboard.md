# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-page Streamlit dashboard (KPI cards, monthly sales trend, category/region breakdowns) reading `data/sales-data.csv`, matching the PRD's Phase 1 scope.

**Architecture:** `calculations.py` holds pure, pytest-tested data functions (loading, totals, aggregations); `app.py` holds Streamlit page config and layout only, calling into `calculations.py` and Plotly chart-builder helpers. No database, no auth, no filtering — Phase 1 only.

**Tech Stack:** Python 3.11+, Streamlit, Pandas, Plotly, pytest.

**Spec:** `docs/superpowers/specs/2026-09-17-sales-dashboard-design.md`

## Global Constraints

- Tech stack is Streamlit + Pandas + Plotly + pytest, Python 3.11+ (PRD Technical Approach).
- Data source is `data/sales-data.csv`, read-only — never modify this file.
- Sales trend chart uses **monthly** granularity, not daily.
- Category and region bar charts are sorted **descending** by `total_amount`.
- Dashboard page title / header text is exactly **"ShopSmart Sales Dashboard"**.
- All data calculations live in `calculations.py` and are unit-tested with pytest under `tests/`. `app.py` holds only Streamlit rendering and chart-building and is not unit-tested (verified manually instead).
- A missing or malformed `data/sales-data.csv` must produce a friendly `st.error(...)` followed by `st.stop()` in `app.py` — never a raw Python traceback.
- Out of scope, no code for: user authentication, real-time database integration, export (PDF/Excel), email alerts, filtering/date-range selection, drill-down to transaction detail, mobile-responsive design.
- Environment is a plain Python virtual environment in `venv/` with `requirements.txt` — no uv, conda, or poetry.
- Run tests with `python -m pytest` (not bare `pytest`) — this adds the project root to `sys.path` so `tests/test_calculations.py` can `import calculations` without extra packaging config (no `__init__.py`, no `conftest.py` needed).
- All work happens on the existing `feature/sales-dashboard` branch — do not create a git worktree.
- Every commit message includes the milestone ID it belongs to (`TASK-1` through `TASK-7`, from `TASKS.md`).
- Deployment (the final task, TASK-7) is executed by the user, not the agent — the plan stops there and hands off.

---

### Task 1: Project scaffolding and environment (Milestone: TASK-1)

**Files:**
- Create: `requirements.txt`
- Create: `app.py`

**Interfaces:**
- Produces: a runnable `app.py` skeleton with `st.set_page_config` and a title, which Task 3 extends with data loading.

- [ ] **Step 1: Create the virtual environment**

Run: `python3 -m venv venv`

- [ ] **Step 2: Create `requirements.txt`**

```
streamlit>=1.38
pandas>=2.2
plotly>=5.24
pytest>=8.3
```

- [ ] **Step 3: Activate the environment and install dependencies**

Run:
```bash
source venv/bin/activate
pip install -r requirements.txt
```
Expected: all four packages install with no errors.

- [ ] **Step 4: Create `app.py` with a minimal page skeleton**

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
```

- [ ] **Step 5: Run the app and confirm it launches**

Run: `streamlit run app.py`
Expected: terminal prints a Local URL (e.g. `http://localhost:8501`); opening it shows a page titled "ShopSmart Sales Dashboard" with no errors in the terminal or browser. Stop the server (Ctrl+C) once confirmed.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt app.py
git commit -m "TASK-1: project scaffolding and environment setup"
```

---

### Task 2: TDD — `load_data` (Milestone: TASK-2)

**Files:**
- Create: `calculations.py`
- Create: `tests/test_calculations.py`

**Interfaces:**
- Produces: `load_data(path: str) -> pd.DataFrame` — reads the CSV with `date` parsed as a datetime column. Raises `FileNotFoundError` if `path` doesn't exist. Used by `app.py` (Task 3) and by every later test in `tests/test_calculations.py` via the `df` fixture defined here.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_calculations.py
import pandas as pd
import pytest

from calculations import load_data


@pytest.fixture
def df():
    return load_data("data/sales-data.csv")


def test_load_data_returns_expected_shape_and_columns():
    result = load_data("data/sales-data.csv")
    assert len(result) == 482
    assert list(result.columns) == [
        "date", "order_id", "product", "category", "region",
        "quantity", "unit_price", "total_amount",
    ]


def test_load_data_parses_date_column_as_datetime():
    result = load_data("data/sales-data.csv")
    assert pd.api.types.is_datetime64_any_dtype(result["date"])


def test_load_data_raises_for_missing_file():
    with pytest.raises(FileNotFoundError):
        load_data("data/does-not-exist.csv")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_calculations.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'calculations'` (the file doesn't exist yet).

- [ ] **Step 3: Implement `load_data`**

```python
# calculations.py
import pandas as pd


def load_data(path):
    return pd.read_csv(path, parse_dates=["date"])
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_calculations.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-2: add load_data with tests"
```

---

### Task 3: Wire data loading into `app.py`, with friendly error handling (Milestone: TASK-2)

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `calculations.load_data(path: str) -> pd.DataFrame` (Task 2)

- [ ] **Step 1: Load data in `app.py` with error handling**

```python
# app.py
import streamlit as st

import calculations

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

try:
    df = calculations.load_data("data/sales-data.csv")
except Exception as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()

st.title("ShopSmart Sales Dashboard")
```

- [ ] **Step 2: Manually verify the happy path**

Run: `streamlit run app.py`
Expected: page loads with the title and no errors, same as Task 1's check (data now loads silently in the background).

- [ ] **Step 3: Manually verify the error path**

Run:
```bash
mv data/sales-data.csv data/sales-data.csv.bak
streamlit run app.py
```
Expected: page shows a red error box reading "Could not load sales data: ..." — not a raw traceback. Then restore the file:
```bash
mv data/sales-data.csv.bak data/sales-data.csv
```

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "TASK-2: wire data loading into app with friendly error handling"
```

---

### Task 4: TDD — `total_sales` and `total_orders` (Milestone: TASK-3)

**Files:**
- Modify: `calculations.py`
- Modify: `tests/test_calculations.py`

**Interfaces:**
- Produces: `total_sales(df: pd.DataFrame) -> float`, `total_orders(df: pd.DataFrame) -> int`. Used by `app.py` in Task 5.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_calculations.py` (update the import line to include the new functions):

```python
from calculations import load_data, total_sales, total_orders
```

```python
def test_total_sales_sums_all_transactions(df):
    assert total_sales(df) == pytest.approx(116500.21, abs=0.01)


def test_total_orders_counts_unique_orders(df):
    assert total_orders(df) == 482
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_calculations.py -v`
Expected: FAIL — `ImportError: cannot import name 'total_sales' from 'calculations'`.

- [ ] **Step 3: Implement the functions**

Add to `calculations.py`:

```python
def total_sales(df):
    return df["total_amount"].sum()


def total_orders(df):
    return df["order_id"].nunique()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_calculations.py -v`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-3: add total_sales and total_orders with tests"
```

---

### Task 5: Render KPI cards (Milestone: TASK-3)

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `calculations.total_sales(df) -> float`, `calculations.total_orders(df) -> int` (Task 4)

- [ ] **Step 1: Add the KPI row to `app.py`**

Add after `st.title(...)`:

```python
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${calculations.total_sales(df):,.0f}")
col2.metric("Total Orders", f"{calculations.total_orders(df):,}")
```

- [ ] **Step 2: Manually verify**

Run: `streamlit run app.py`
Expected: two metric cards showing "Total Sales: $116,500" and "Total Orders: 482", side by side.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "TASK-3: render KPI cards"
```

---

### Task 6: TDD — `monthly_trend` (Milestone: TASK-4)

**Files:**
- Modify: `calculations.py`
- Modify: `tests/test_calculations.py`

**Interfaces:**
- Produces: `monthly_trend(df: pd.DataFrame) -> pd.DataFrame` with columns `["date", "total_amount"]`, one row per calendar month present in the data, `date` as the first-of-month `Timestamp`, sorted chronologically ascending. Used by `app.py` in Task 7.

- [ ] **Step 1: Write the failing test**

Update the import line in `tests/test_calculations.py`:

```python
from calculations import load_data, total_sales, total_orders, monthly_trend
```

```python
def test_monthly_trend_aggregates_by_month_chronologically(df):
    result = monthly_trend(df)
    assert list(result.columns) == ["date", "total_amount"]
    assert len(result) == 12
    assert result["date"].is_monotonic_increasing
    first, last = result.iloc[0], result.iloc[-1]
    assert first["date"] == pd.Timestamp("2024-01-01")
    assert first["total_amount"] == pytest.approx(7175.17, abs=0.01)
    assert last["date"] == pd.Timestamp("2024-12-01")
    assert last["total_amount"] == pytest.approx(15186.34, abs=0.01)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_calculations.py -v`
Expected: FAIL — `ImportError: cannot import name 'monthly_trend' from 'calculations'`.

- [ ] **Step 3: Implement `monthly_trend`**

Add to `calculations.py`:

```python
def monthly_trend(df):
    monthly = (
        df.groupby(df["date"].dt.to_period("M"))["total_amount"]
        .sum()
        .reset_index()
    )
    monthly["date"] = monthly["date"].dt.to_timestamp()
    return monthly.sort_values("date").reset_index(drop=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_calculations.py -v`
Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-4: add monthly_trend with test"
```

---

### Task 7: Build and render the sales trend chart (Milestone: TASK-4)

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `calculations.monthly_trend(df) -> pd.DataFrame` (Task 6)

- [ ] **Step 1: Add the chart-builder helper and import Plotly Express**

Add near the top of `app.py`:

```python
import plotly.express as px
```

Add a helper function (above the page-rendering code):

```python
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
```

- [ ] **Step 2: Render the chart**

Add after the KPI row:

```python
st.plotly_chart(trend_line_chart(calculations.monthly_trend(df)), use_container_width=True)
```

- [ ] **Step 3: Manually verify**

Run: `streamlit run app.py`
Expected: a line chart below the KPI cards with 12 monthly points (Jan–Dec 2024), rising toward December; hovering over a point shows its exact month and dollar value.

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "TASK-4: add sales trend chart"
```

---

### Task 8: TDD — `sales_by_category` and `sales_by_region` (Milestone: TASK-5)

**Files:**
- Modify: `calculations.py`
- Modify: `tests/test_calculations.py`

**Interfaces:**
- Produces: `sales_by_category(df) -> pd.DataFrame` with columns `["category", "total_amount"]`, sorted descending by `total_amount`. `sales_by_region(df) -> pd.DataFrame` with columns `["region", "total_amount"]`, sorted descending by `total_amount`. Used by `app.py` in Task 9.

- [ ] **Step 1: Write the failing tests**

Update the import line in `tests/test_calculations.py`:

```python
from calculations import (
    load_data, total_sales, total_orders, monthly_trend,
    sales_by_category, sales_by_region,
)
```

```python
def test_sales_by_category_sorted_descending(df):
    result = sales_by_category(df)
    assert list(result.columns) == ["category", "total_amount"]
    assert list(result["category"]) == [
        "Electronics", "Wearables", "Audio", "Smart Home", "Accessories",
    ]
    assert result.iloc[0]["total_amount"] == pytest.approx(42683.67, abs=0.01)


def test_sales_by_region_sorted_descending(df):
    result = sales_by_region(df)
    assert list(result.columns) == ["region", "total_amount"]
    assert list(result["region"]) == ["North", "West", "East", "South"]
    assert result.iloc[0]["total_amount"] == pytest.approx(38857.24, abs=0.01)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_calculations.py -v`
Expected: FAIL — `ImportError: cannot import name 'sales_by_category' from 'calculations'`.

- [ ] **Step 3: Implement the functions**

Add to `calculations.py`:

```python
def sales_by_category(df):
    result = df.groupby("category")["total_amount"].sum().reset_index()
    return result.sort_values("total_amount", ascending=False).reset_index(drop=True)


def sales_by_region(df):
    result = df.groupby("region")["total_amount"].sum().reset_index()
    return result.sort_values("total_amount", ascending=False).reset_index(drop=True)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_calculations.py -v`
Expected: 8 passed.

- [ ] **Step 5: Commit**

```bash
git add calculations.py tests/test_calculations.py
git commit -m "TASK-5: add sales_by_category and sales_by_region with tests"
```

---

### Task 9: Build and render category and region bar charts (Milestone: TASK-5)

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `calculations.sales_by_category(df) -> pd.DataFrame`, `calculations.sales_by_region(df) -> pd.DataFrame` (Task 8)

- [ ] **Step 1: Add the chart-builder helpers**

Add below `trend_line_chart`:

```python
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
```

- [ ] **Step 2: Render the charts side by side**

Add after the trend chart:

```python
col3, col4 = st.columns(2)
col3.plotly_chart(category_bar_chart(calculations.sales_by_category(df)), use_container_width=True)
col4.plotly_chart(region_bar_chart(calculations.sales_by_region(df)), use_container_width=True)
```

- [ ] **Step 3: Manually verify**

Run: `streamlit run app.py`
Expected: two bar charts side by side below the trend chart. Category chart bars descend Electronics → Wearables → Audio → Smart Home → Accessories. Region chart bars descend North → West → East → South. Hovering over a bar shows its exact dollar value.

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "TASK-5: add category and region breakdown charts"
```

---

### Task 10: Full verification pass against the PRD (Milestone: TASK-6)

**Files:** none (verification only; fix forward in `app.py` / `calculations.py` if something fails)

- [ ] **Step 1: Run the full test suite**

Run: `python -m pytest -v`
Expected: 8 passed, 0 failed.

- [ ] **Step 2: Run the app and check every PRD acceptance criterion by eye**

Run: `streamlit run app.py`, open the Local URL, and check each item from the PRD's Acceptance Criteria section against the running page:
- Total Sales and Total Orders are displayed prominently
- Line chart shows sales over time with correct data
- Bar chart shows sales by category, sorted highest to lowest
- Bar chart shows sales by region, sorted highest to lowest
- All values match the PRD's Expected Output table (~$116,500, 482 orders, Electronics as top category)
- No errors or warnings appear in the terminal or the browser
- The page looks presentable: consistent spacing, readable labels, no raw column names or truncated text

- [ ] **Step 3: Fix anything that fails, re-run, and commit**

If step 2 surfaces an issue, fix it in `app.py` or `calculations.py`, re-run step 1 and step 2 until both pass cleanly, then commit:

```bash
git add -A
git commit -m "TASK-6: verification and polish"
```

If nothing needed fixing, skip the commit (nothing to save).

---

### Task 11: Deployment to Streamlit Community Cloud (Milestone: TASK-7)

**This task is executed by the user, not the agent.** After the branch is reviewed and merged to `main`, deploy from there:

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
2. Click **New app**, select your repository and the `main` branch, and set the main file path to `app.py`.
3. Click **Deploy**. Streamlit Cloud installs from `requirements.txt` and starts the app.
4. Once live, open the public URL and re-check the PRD's Acceptance Criteria against the deployed version (same checklist as Task 10, Step 2), plus: the page loads within 5 seconds (NFR-1) and shows no errors.
5. Record the public URL wherever your course asks you to submit it.

No plan steps are executed here by the agent — this task exists so the milestone appears in the plan and can be checked off once you've done it yourself.

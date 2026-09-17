# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A tutorial project: build and deploy a Streamlit sales dashboard (`app.py`) following a
PRD → `TASKS.md` → brainstorm → plan → implement → commit → push → review → deploy workflow.
The dashboard itself (`prd/ecommerce-analytics.md`) is simple; the point of the repo is the
workflow. Design/implementation-plan docs for the current build live under
`docs/superpowers/plans/` and `docs/superpowers/specs/`.

## Commands

```bash
source venv/bin/activate          # plain venv — no uv/conda/poetry
pip install -r requirements.txt

python -m pytest                  # run all tests (NOT bare `pytest` — see below)
python -m pytest -v
python -m pytest tests/test_calculations.py::test_total_sales_sums_all_transactions

streamlit run app.py --server.headless true   # see note below on --server.headless
```

- Use `python -m pytest`, not bare `pytest`: it adds the project root to `sys.path` so
  `tests/test_calculations.py` can `import calculations` with no `__init__.py`/`conftest.py`.
- Always pass `--server.headless true` (see Lessons below).
- Check `lsof -ti :8501` before starting a new instance — a prior run left listening is a
  common source of `Port 8501 is not available`.

## Architecture

- **`calculations.py`** — all data logic: loading the CSV and every aggregation
  (`load_data`, `total_sales`, `total_orders`, `monthly_trend`, `sales_by_category`,
  `sales_by_region`). Pure functions on plain pandas objects, no formatting. The one
  exception is `load_data`, which is decorated with `@st.cache_data` (so it needs
  `import streamlit`) to avoid re-reading the CSV on every Streamlit rerun — every other
  function stays free of Streamlit imports. This is the only file covered by
  `tests/test_calculations.py`.
- **`app.py`** — Streamlit page config, layout, and Plotly chart-builder helpers
  (`trend_line_chart`, `category_bar_chart`, `region_bar_chart`). Calls into
  `calculations.py` for all numbers; never computes aggregates itself. Not unit-tested —
  verified by running the app and checking it by eye against the PRD's acceptance criteria.
- **`data/sales-data.csv`** — read-only sample data (482 rows, 12 months, 5 categories,
  4 regions). Never modify this file.
- **`TASKS.md`** — the milestone board (`TASK-1` … `TASK-7`), with To Do / In Progress /
  Done columns. Every commit message includes the milestone ID it belongs to, so `git log`
  traces requirement → code → deployment. Update this file as milestones move, per its own
  Definition of Done section.

## Project-specific constraints (from the implementation plan)

- Tech stack is fixed: Streamlit + Pandas + Plotly + pytest, Python 3.11+.
- Sales trend chart is **monthly** granularity, not daily.
- Category/region bar charts are sorted **descending** by `total_amount`.
- Page title/header text is exactly **"ShopSmart Sales Dashboard"**.
- A missing/malformed `data/sales-data.csv` must produce a friendly `st.error(...)` followed
  by `st.stop()` — never a raw traceback.
- Out of scope (Phase 2, do not build): auth, real-time DB integration, export, email
  alerts, filtering/date-range selection, drill-down, mobile-responsive design.
- Deployment (TASK-7, Streamlit Community Cloud) is done by the user from `main` after
  merge — not something to execute from an agent session.

## Lessons

Rules distilled from the "Notes" recorded against milestones in `TASKS.md` as they're
completed — read that file's Done section for the full incident behind each one.

- Never run `streamlit run app.py` without `--server.headless true`. Without it, the
  default (non-headless) invocation can block on an interactive onboarding email prompt
  with no stdin available and exit with code 255.

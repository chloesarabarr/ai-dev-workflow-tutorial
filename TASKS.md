# Tasks

This file tracks all work for the E-Commerce Analytics dashboard, from initial setup through deployment.

## Definition of Done

A milestone can only move to Done when:

- Acceptance criteria met
- App runs locally with `streamlit run app.py`
- Changes committed with the milestone ID in the message

## To Do

### TASK-3: KPI cards implementation
Display Total Sales and Total Orders as prominent KPI cards.
- [ ] Total Sales displayed as formatted currency (~$116,500)
- [ ] Total Orders displayed as formatted count (482)
- [ ] KPIs displayed prominently at the top of the dashboard

Commit:

### TASK-4: Sales trend chart
Add a line chart showing sales over time.
- [ ] Line chart shows sales over time with correct data
- [ ] Interactive tooltips show exact values
- [ ] Chart renders within 2 seconds of data load

Commit:

### TASK-5: Category and region breakdowns
Add bar charts for sales by category and by region.
- [ ] Bar chart shows sales by category, sorted highest to lowest, all categories shown
- [ ] Bar chart shows sales by region, sorted highest to lowest, all regions shown
- [ ] Interactive tooltips with exact values on both charts

Commit:

### TASK-6: Testing and refinement
Verify the dashboard against the PRD's acceptance criteria and polish the presentation.
- [ ] Dashboard runs without errors or warnings
- [ ] All displayed values match expected calculations from the CSV
- [ ] Professional appearance suitable for an executive presentation

Commit:

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the dashboard and share a public URL.
- [ ] App deployed and accessible via a public shareable URL
- [ ] Deployed dashboard loads within 5 seconds
- [ ] Deployed version verified to match local version (no errors)

Commit:

## In Progress

## Done

### TASK-2: Data loading and basic structure
Load `sales-data.csv` into a Pandas DataFrame and scaffold the page layout.
- [x] CSV loads without errors; date, numeric, and categorical columns parsed correctly
- [x] Basic page title/layout scaffolded in Streamlit

Commit: b9c3d34, 3e33617

### TASK-1: Environment setup and project initialization
Set up the project structure and install dependencies (Streamlit, Pandas, Plotly).
- [x] Project structure created (`app.py`, `data/`, `requirements.txt`)
- [x] Dependencies installed and importable
- [x] `streamlit run app.py` launches a placeholder app with no errors

Commit: e1595c0
Notes: on this machine's first-ever `streamlit run`, the default (non-headless) invocation blocked on an interactive onboarding email prompt with no stdin available and exited with code 255; fixed by running with `--server.headless true`, which is now the standard way this project runs the app.

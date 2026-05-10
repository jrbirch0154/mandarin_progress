# Mandarin Progress Tracker

A personal Streamlit dashboard for tracking my Mandarin Chinese comprehensible input. It visualizes my daily listening sessions, consistency trends, and cumulative progress towards hour milestones.

**Live app:** [mandarin-progress.streamlit.app](https://mandarin-progress.streamlit.app/)

---

## Overview

This app ingests a personal CSV log of daily Mandarin input sessions (in minutes) and renders an interactive Plotly dashboard with several charts and summary metrics. Data is fetched from a remote URL stored as a Streamlit secret, cached for 5 minutes, and displayed with a clean, wide-layout UI.

The tracker focuses on data recorded from **January 2, 2026 onward**. This is the point at which I began to study seriously.

---

## Features

- **Cumulative hours line chart** - filled area chart of total hours over time, with horizontal reference lines for each fluency level milestone
- **Daily input bar chart** - color-coded by whether the 30-minute daily target was met, with a 7-day rolling average overlay
- **Monthly hours bar chart** - aggregated input per month with a red-to-blue color scale
- **Day-of-week violin plot** - distribution of daily input by weekday to identify consistency patterns
- **Summary metrics** - total hours, best day, start date, days elapsed, and overall daily average vs. target
- **CSV export** - one-click download of the underlying data

---

## Fluency Milestones

Input hours are benchmarked against a simplified level scale. (Twice the level scale I used while learning Spanish.)

| Level | Hours |
|-------|-------|
| 1     | 0     |
| 1.5   | 25    |
| 2     | 100   |
| 3     | 300   |
| 4     | 600   |
| 5     | 1,200 |
| 6     | 2,000 |
| 7     | 3,000 |

---

## Setup

### Requirements

```
pandas
streamlit
plotly
```

Install with:

```bash
pip install -r requirements.txt
```

### Secrets

The app reads the CSV data URL from Streamlit secrets. Create a `.streamlit/secrets.toml` file:

```toml
URL = "https://your-data-url-here.csv"
```

The CSV must contain at minimum:
- `Date` - date of the session
- `Input (Min)` - minutes of input for that day

### Running locally

```bash
streamlit run mandarin_progress.py
```
---

## Notes

- Data is cached for 5 minutes (`@st.cache_data(ttl=300)`) to avoid redundant fetches
- The daily target is set to **30 minutes**. This constant is easily adjustable at the top of the script
- Sessions before January 2, 2026 are filtered out as pre-serious-study data

# Mandarin Progress
# Sun Apr 26 22:08:17 2026
# Jacob Birch

"""
This will scrape mandarin progress and format a graph. Returns an HTML
"""

# %% Initializing


import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"
pio.templates.default = "presentation"
# from scipy import stats

URL = st.secrets["URL"]

DAILY_TARGET = 30  # minutes

MILESTONES = {
    "1": 0,
    "1.5": 25,
    "2": 100,
    "3": 300,
    "4": 600,
    "5": 1200,
    "6": 2000,
    "7": 3000,
}


@st.cache_data(ttl=(60 * 5))  # cache data for 5 min
def init(URL=URL) -> pd.DataFrame:
    df = pd.read_csv(URL, low_memory=False)
    # df = df.drop('Notes',axis=1) # already deleted
    df = df.dropna(subset="Input (Min)")
    df["Total (H)"] = df["Input (Min)"].cumsum() / 60

    # %% DF Work

    df["Date"] = pd.to_datetime(df["Date"])
    df = df[
        df["Date"] >= "2026-01-02"
    ]  # before 1/1/26 I didn't take it seriously
    df["Level"] = pd.cut(
        df["Total (H)"],
        bins=list(MILESTONES.values()),
        labels=list(MILESTONES.keys())[:-1],  # drop 1, use 2-7
        include_lowest=True,
    )

    df["met_target"] = df["Input (Min)"] >= DAILY_TARGET

    df["rolling_avg"] = df["Input (Min)"].rolling(7).mean()

    df["target_rolling"] = df["met_target"].rolling(7).mean() * 100

    return df


# %% Line Plot
def line_plot(df):
    fig = px.line(
        df,
        x="Date",
        y="Total (H)",
        title="Mandarin Hours over Time",
    )

    fig.update_traces(
        fill="tozeroy", fillcolor="rgba(0,0,0,.1)", line_width=2.5
    )

    fig.update_layout(xaxis_title="Date", yaxis_title="Hours")

    for key, value in MILESTONES.items():
        fig.add_hline(
            y=value,
            line_dash="dash",
            line_width=0.5,
            annotation_text=f"Level {key}",
            annotation_position="top right",
        )

    fig.update_yaxes(range=[0, 110])

    return fig


# %% Bar plot


def bar_plot(df):
    fig2 = px.bar(
        df,
        x="Date",
        y="Input (Min)",
        title="Mandarin Input over Time",
        color="met_target",
        color_discrete_map={True: "#4C9BE8", False: "#F4A261"},
    )

    fig2.update_traces(hovertemplate="%{x}<br> %{y:.0f} minutes")

    fig2.add_hline(
        y=DAILY_TARGET, line_dash="dash", line_width=0.5, line_color="red"
    )
    # annotation_text='Daily Target (30 min)',annotation_position='top left', annotation_xshift=50, annotation_yshift=100)

    fig2.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["rolling_avg"],
            line=dict(width=2, color="black"),
            name="Rolling Average (7d)",
            hovertemplate="Date: %{x}<br>7 Day Rolling Avg: %{y:.1f} min<extra></extra>",
        )
    )

    fig2.update_layout(
        xaxis_title="Date", yaxis_title="Input (M)", showlegend=False
    )

    fig2.update_xaxes(range=["2026-01-01", df["Date"].max()])

    return fig2


# %% Violin plot


def violin_plot(df):

    fig3 = go.Figure()

    day = df["Date"].dt.day_name()
    day_order = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]

    fig3.add_trace(
        go.Violin(
            y=df["Input (Min)"],
            x=day,
            box_visible=True,
            meanline_visible=True,
            name="Daily Input",
        )
    )

    fig3.update_traces(spanmode="hard")

    fig3.update_layout(title="Input Violin", yaxis_title="Input [M]")

    fig3.update_xaxes(categoryorder="array", categoryarray=day_order)
    fig3.update_yaxes(range=[0, df["Input (Min)"].max() + 1])

    return fig3


# %% Consistency Plot


def consist_plot(df):
    fig4 = px.line(
        df, x="Date", y="target_rolling", title="Mandarin Input Consistency"
    )

    fig4.update_traces(hovertemplate="%{x}<br>%{y:.1f}%")

    fig4.update_layout(
        xaxis_title="Date", yaxis_title="30 minute consistency (%)"
    )

    overall_avg = df["target_rolling"].mean()

    fig4.add_hline(
        y=overall_avg,
        annotation_text="Overall Average",
        annotation_position="top left",
    )

    fig4.add_hline(
        y=(3 / 7) * 100,
        line_color="red",
        line_dash="dash",
        annotation_text="3/7 days",
    )

    return fig4


# %% Main

if __name__ == "__main__":

    st.set_page_config(page_title="Mandarin Progress Tracker", layout="wide")

    st.title("Mandarin Progress Tracker")

    if st.button("Run"):
        try:
            df = init()
            csv = df.to_csv(index=False)
            st.success("Data found")

            start_date = df["Date"].min().strftime("%Y-%m-%d")
            days_since_started = (df["Date"].max() - df["Date"].min()).days
            best_row = df.loc[df["Input (Min)"].idxmax()]
            best_day = best_row["Date"].strftime("%Y-%m-%d")
            best_day_minutes = best_row["Input (Min)"]
            overall_avg = df['Input (Min)'].mean()

            line = line_plot(df)
            bar = bar_plot(df)
            violin = violin_plot(df)
            const = consist_plot(df)

            col1, col2 = st.columns(2)
            with col1:
                st.metric(f"Total Hours: {df['Total (H)'].max():.1f}")
                st.metric('Best day:',value=best_day,delta=best_day_minutes)
            with col2:
                st.metric("Start date:",value=start_date, delta=days_since_started)
                st.metric('Overall avg:',value=overall_avg,delta=overall_avg-DAILY_TARGET)

            for i in [line, bar, violin, const]:
                st.plotly_chart(i)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name="mandarin_data.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.error(f"Error: {e}")

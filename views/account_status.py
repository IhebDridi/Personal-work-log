import streamlit as st
import pandas as pd
import plotly.express as px
import calplot
import matplotlib.pyplot as plt
from shift_management.db import get_user_shifts
from shift_management.logic import calc_account_stats

def gantt_chart_view(df):
    df = df.copy()
    # Ensure Date is datetime
    if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Date"] = pd.to_datetime(df["Date"])
    df['shift_start'] = pd.to_datetime(df["Date"].dt.strftime("%Y-%m-%d") + " " + df["Start"])
    df['shift_end'] = pd.to_datetime(df["Date"].dt.strftime("%Y-%m-%d") + " " + df["Actual End"])
    df = df.sort_values("shift_start")
    fig = px.timeline(
        df,
        x_start="shift_start",
        x_end="shift_end",
        y="Date",
        color="Worked (h)",
        title="Your Daily Shift Timeline (Gantt Chart)",
        labels={"Worked (h)": "Hours Worked"}
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

def calendar_heatmap_view(df):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    hours_per_day = df.groupby("Date")["Worked (h)"].sum()
    fig, ax = calplot.calplot(
        hours_per_day,
        cmap="YlGn",
        colorbar=True,
        suptitle="Workload Calendar",
        figsize=(14, 3)
    )
    st.pyplot(fig)

def run(username, settings):
    # Get all shifts & summary data
    shifts = get_user_shifts(username)
    vdays = int(settings.get('vacation_days', 20))
    n_shifts, total_overtime, total_normal, vacation_days_left, vacations_used = calc_account_stats(shifts, vdays)
    st.markdown(f"""
    **Shifts worked**: {n_shifts}  
    **Total overtime hours**: {total_overtime:.2f}  
    **Total normal hours**: {total_normal:.2f}  
    **Vacation days used**: {vacations_used}  
    **Vacation days left**: {vacation_days_left}
    """)

    # Build dataframe for visuals
    columns = ["ID", "Date", "Start", "Scheduled End", "Actual End", "Worked (h)", "Overtime (h)", "Vacation", "Unpaid Vacation"]
    df = pd.DataFrame(shifts, columns=columns)

    if not df.empty:
        st.markdown("### 📈 Visualizations")
        # Gantt Chart
        gantt_chart_view(df)
        # Calendar Heatmap
        calendar_heatmap_view(df)
        
        # (Optional: old charts, e.g. pie/bar, can go here too)
    else:
        st.info("No shift data yet. Add your first shift!")
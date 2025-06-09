import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from shift_management.db import get_user_shifts
from shift_management.logic import calc_account_stats

def gantt_chart_view(df):
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Date"] = pd.to_datetime(df["Date"])
    df['shift_start'] = pd.to_datetime(df["Date"].dt.strftime("%Y-%m-%d") + " " + df["Start"])
    df['shift_end'] = pd.to_datetime(df["Date"].dt.strftime("%Y-%m-%d") + " " + df["Actual End"])
    df["Worked (h)"] = df["Worked (h)"].round(2)
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
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    mask = (df["Date"].dt.year == current_year) & (df["Date"].dt.month == current_month)
    df_month = df[mask]
    hours_per_day = df_month.groupby("Date")["Worked (h)"].sum()
    if not hours_per_day.empty:
        import calplot
        import matplotlib.pyplot as plt
        fig, ax = calplot.calplot(
            hours_per_day,
            cmap="YlGn",
            colorbar=True,
            suptitle=f"Workload Calendar ({now.strftime('%B %Y')})",
            figsize=(14, 3)
        )
        st.pyplot(fig)
    else:
        st.info("No data for this month yet.")

def run(username, settings):
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

    columns = ["ID", "Date", "Start", "Scheduled End", "Actual End", "Worked (h)", "Overtime (h)", "Vacation", "Unpaid Vacation"]
    df = pd.DataFrame(shifts, columns=columns)

    if not df.empty:
        st.markdown("### 📈 Visualizations")
        gantt_chart_view(df)
        calendar_heatmap_view(df)
    else:
        st.info("No shift data yet. Add your first shift!")
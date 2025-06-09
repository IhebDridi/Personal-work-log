import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import calendar
import matplotlib.pyplot as plt
from shift_management.db import get_user_shifts
from shift_management.logic import calc_account_stats


def gantt_chart_view(df):
    import plotly.express as px
    import numpy as np

    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Date"] = pd.to_datetime(df["Date"])
    now = datetime.now()
    # Filter to current month
    df = df[(df["Date"].dt.year == now.year) & (df["Date"].dt.month == now.month)]

    # Day number as a string, with leading zeros for better visual sorting (or as int for natural sorting)
    df['Day'] = df["Date"].dt.day.astype(int)
    df['shift_start'] = pd.to_datetime(df["Date"].dt.strftime("%Y-%m-%d") + " " + df["Start"])
    df['shift_end'] = pd.to_datetime(df["Date"].dt.strftime("%Y-%m-%d") + " " + df["Actual End"])
    df["Worked (h)"] = df["Worked (h)"].round(2)

    # Sort from last day to first day, so most recent on top
    df = df.sort_values("Day", ascending=False)

    fig = px.timeline(
        df,
        y="Day",                     # days of month on y axis
        x_start="shift_start",
        x_end="shift_end",
        color="Worked (h)",          # Color by worked hours
        title=f"Shifts by Day of Month ({now.strftime('%B %Y')})",
        labels={"Worked (h)": "Hours Worked"},
        hover_data=["Start", "Actual End", "Worked (h)", "Date"],
        color_continuous_scale=px.colors.sequential.YlOrBr
    )
    fig.update_layout(
        yaxis=dict(autorange='reversed'),  # puts today at the top
        xaxis_title='Time of Day',
        yaxis_title='Day of Month',
        bargap=0.1
    )
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)



def month_calendar_heatmap(df, year=None, month=None, value_col="Worked (h)"):
    if year is None or month is None:
        d = datetime.now()
        year, month = d.year, d.month

    # Filter DataFrame to current month/year
    df["Date"] = pd.to_datetime(df["Date"])
    mask = (df["Date"].dt.year == year) & (df["Date"].dt.month == month)
    dfm = df[mask]

    # Aggregate values by day
    values = dfm.groupby(dfm["Date"].dt.day)[value_col].sum().to_dict()

    cal = calendar.monthcalendar(year, month)
    weeks = len(cal)
    arr = np.full((weeks, 7), np.nan)  # fill with NaN
    for i, week in enumerate(cal):
        for j, day in enumerate(week):
            if day > 0:
                arr[i, j] = values.get(day, 0)

    # Plot
    fig, ax = plt.subplots(figsize=(9, weeks+1))
    cmap = plt.get_cmap("YlGn")
    im = ax.imshow(arr, cmap=cmap, vmin=0)
    # Add days of week
    ax.set_xticks(np.arange(7))
    ax.set_xticklabels(list(calendar.day_abbr))
    # Add day numbers
    for i in range(arr.shape[0]):
        for j in range(7):
            day_nr = cal[i][j]
            if day_nr != 0:
                txt = str(int(day_nr))
                color = "black" if np.isnan(arr[i, j]) or arr[i, j] < (np.nanmax(arr)/2) else "white"
                ax.text(j, i, f"{txt}\n{arr[i, j]:.2f}" if arr[i, j] else txt, va='center', ha='center', color=color, fontsize=10)
    # Label title
    month_name = calendar.month_name[month]
    ax.set_title(f"Workload Heatmap - {month_name} {year}")
    ax.set_yticks([])
    plt.colorbar(im, ax=ax, shrink=0.7)
    plt.tight_layout()
    return fig



def calendar_heatmap_view(df):
    now = datetime.now()
    if not df.empty:
        fig = month_calendar_heatmap(df, year=now.year, month=now.month, value_col="Worked (h)")
        st.pyplot(fig)
    else:
        st.info("No data for this month yet.")

def run(username, settings):
    # 1. Get data and assemble DataFrame
    shifts = get_user_shifts(username)
    columns = ["ID", "Date", "Start", "Scheduled End", "Actual End", "Worked (h)", "Overtime (h)", "Vacation", "Unpaid Vacation"]
    df = pd.DataFrame(shifts, columns=columns)

    # 2. Stats
    vdays = int(settings.get('vacation_days', 20))
    n_shifts, total_overtime, total_normal, vacation_days_left, vacations_used = calc_account_stats(shifts, vdays)
    st.markdown(f"""
    **Shifts worked**: {n_shifts}  
    **Total overtime hours**: {total_overtime:.2f}  
    **Total normal hours**: {total_normal:.2f}  
    **Vacation days used**: {vacations_used}  
    **Vacation days left**: {vacation_days_left}
    """)

    # 3. Charts: only if df is not empty
    if not df.empty:
        st.markdown("### 📈 Visualizations")
        gantt_chart_view(df)
        dnow = datetime.now()
        fig = month_calendar_heatmap(df, year=dnow.year, month=dnow.month, value_col="Worked (h)")
        st.pyplot(fig)
    else:
        st.info("No shift data yet. Add your first shift!")
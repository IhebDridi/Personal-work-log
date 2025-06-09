import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from shift_management.db import get_user_shifts
from shift_management.logic import calc_account_stats

def gantt_chart_view(df):
    # ... as before ...

def month_calendar_heatmap(df, year=None, month=None, value_col="Worked (h)"):
    # ... as before ...

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
        # --- calendar heatmap for current month
        dnow = datetime.now()
        fig = month_calendar_heatmap(df, year=dnow.year, month=dnow.month, value_col="Worked (h)")
        st.pyplot(fig)
    else:
        st.info("No shift data yet. Add your first shift!")
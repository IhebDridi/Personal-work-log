import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from shift_management.db import get_user_shifts
from shift_management.logic import calc_account_stats

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

    if len(shifts) > 0:
        columns = ["ID", "Date", "Start", "Scheduled End", "Actual End",
                   "Worked (h)", "Overtime (h)", "Vacation", "Unpaid Vacation"]
        df = pd.DataFrame(shifts, columns=columns)
        # Pie chart
        pie_data = [max(total_normal, 0), max(total_overtime, 0)]
        labels = ['Normal Hours', 'Overtime Hours']
        fig = go.Figure(data=[go.Pie(labels=labels, values=pie_data, hole=.3)])
        fig.update_traces(marker=dict(colors=['royalblue', 'deeppink']))
        st.plotly_chart(fig, use_container_width=True)
        # Bar plot
        df_sorted = df.sort_values("Date").tail(10)
        st.write("**Recent Overtime Per Shift (last 10):**")
        barfig = go.Figure()
        barfig.add_trace(go.Bar(
            x=df_sorted["Date"],
            y=df_sorted["Overtime (h)"],
            marker_color="deeppink",
            name="Overtime (h)"
        ))
        st.plotly_chart(barfig, use_container_width=True)
    else:
        st.info("No shifts available for charting yet.")